from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.db import models
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from user_messages import api as user_messages
from user_messages.models import Message


def set_default_site_id():
    return Site.objects.get_current()

def set_default_message():
    default = {
        "title": "",
        "description": "",
        "accept_button": "Accept",
        "accept_url": "user_notifications:notification-confirm",
        "decline_button": "Decline",
        "decline_url": "user_notifications:notification-decline"
    }
    return default

class DisplayType(models.IntegerChoices):
    BOOTSTRAP_ALERT = 100, _("Bootstrap Alert")
    MODAL_INFO = 200, _("Modal Info")
    MODAL_FORM = 201, _("Modal Form")
    ACTIVITY_FEED = 300, _("Activity Feed")
    # REDIRECT expects a "redirect_to" attribute in the message
    # which can be a url path or a route path name for reverse
    REDIRECT = 400, _("Redirect") 


class Notification(models.Model):
    """
    Class that helps creating site wide notifications.
    Notifications can be displayed as a Bootstrap Alert or as a Bootstrap Modal.
    One can choose to show the message to the user once or on every view until the user takes action.
    One can choose to show the message from or to a certain date with start and end date.
    One can choose to add additional rules implemented by the developer by using the RuleBase Class
    The notification has a JSON filed called message with the following default attributes:
        title: <Title for the modal (Ignored by the bootstrap Alert)>
        description: <The modal body or alert description>
        accept_button: <Text inside the accept button in the modal (Ignored by the bootstrap Alert)>
        accept_url: <POST path for a user if they decide to accept the notification (Ignored by the bootstrap Alert)>
        decline_button: <Text inside the decline button in the modal (Ignored by the bootstrap Alert)>
        accept_url: <POST path for a user if they decide to decline the notification (Ignored by the bootstrap Alert)>
    """
    name = models.CharField(verbose_name=_("Notification Name"), blank=False, null=False, max_length=65)
    active = models.BooleanField(verbose_name=_("Active"), default=False)
    sites = models.ManyToManyField(Site, verbose_name=_("Sites"), blank=True, related_name="notifications")
    display_type = models.IntegerField(verbose_name=_("Message Type"), choices=DisplayType.choices, default=DisplayType.BOOTSTRAP_ALERT)
    message = models.JSONField(verbose_name=_("Message Content"), blank=True, null=True, default=set_default_message)
    deliver_once = models.BooleanField(verbose_name=_("Deliver Once"), default=True)
    start_date = models.DateTimeField(_("Start Date"), blank=True, null=True, help_text=_("Notification Start Date?"))
    end_date = models.DateTimeField(_("End Date"), blank=True, null=True, help_text=_("Notification End Date?"))
    rules = models.JSONField(default=list, blank=True, null=True)
    meta = models.JSONField(default=dict, blank=True, null=True)

    objects = models.Manager()
    on_site = CurrentSiteManager()

    def __str__(self):
        return self.name

    def add_user_message(self, user, site_id=None):
        self.message['display_type'] = self.display_type
        self.message['pk'] = self.pk
        if site_id:
            self.message['site_id'] = site_id
        user_messages.info(user, self.name, deliver_once=self.deliver_once, meta=self.message)
    
    def already_exists(self, user):
        if Message.objects.filter(user=user, message=self.name).count():
            return True
        return False

    def is_between_dates(self):
        if not self.start_date and not self.end_date:
            return True
        elif (not self.start_date or timezone.now() > self.start_date) and (not self.end_date or timezone.now() < self.end_date):
            return True
        return False

    def save_accepted(self, user, site):
        if 'accepted' not in self.meta.keys():
            self.meta['accepted'] = dict()

        if site.domain not in self.meta['accepted'].keys():
            self.meta['accepted'][site.domain] = dict()

        if user.username not in self.meta['accepted'][site.domain].keys():
            self.meta['accepted'][site.domain][user.username] = list()

        self.meta['accepted'][site.domain][user.username].append(f"{timezone.now():%Y-%m-%d %H:%M:%S}")
        self.save()

    def save_declined(self, user, site):
        if 'declined' not in self.meta.keys():
            self.meta['declined'] = dict()

        if site.domain not in self.meta['declined'].keys():
            self.meta['declined'][site.domain] = dict()

        if user.username not in self.meta['declined'][site.domain].keys():
            self.meta['declined'][site.domain][user.username] = list()

        self.meta['declined'][site.domain][user.username].append(f"{timezone.now():%Y-%m-%d %H:%M:%S}")
        self.save()

    def save_user_acknowledgement(self, user, site, accepted):
        if self.deliver_once:
            return None     # Notifications should be deliver_once=False to work as an ack
        try:
            user_message = Message.objects.get(user=user, message=self.name, deliver_once=False, delivered_at__isnull=True)
        except ObjectDoesNotExist as error:
            return None
        except MultipleObjectsReturned as error:
            user_message = Message.objects.filter(user=user, message=self.name, deliver_once=False, delivered_at__isnull=True).order_by('created_at').first()

        user_message.delivered_at = timezone.now()
        user_message.deliver_once = True
        user_message.save()
        if accepted:
            self.save_accepted(user, site)
        else:
            self.save_declined(user, site)

