from datetime import timedelta
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.utils import timezone
from django.test import TestCase, Client
from user_messages.models import Message
from user_notifications.models import Notification

User = get_user_model()

# Create your tests here.
class NotificationModelTests(TestCase):

    fixtures = ['user', 'unit_test']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(pk=1)
        self.client.force_login(self.user)

    def test_queue_expire_after_date(self):
        notification = Notification.objects.get(pk=3)
        self.assertTrue(notification.is_between_dates)

    def test_dont_queue_expire_after_date(self):
        notification = Notification.objects.get(pk=3)
        notification.end_date = (timezone.now() - timedelta(days=1))
        self.assertFalse(notification.is_between_dates())

    def test_queue_start_after_date(self):
        notification = Notification.objects.get(pk=4)
        self.assertTrue(notification.is_between_dates())

    def test_dont_queue_start_after_date(self):
        notification = Notification.objects.get(pk=4)
        notification.start_date = (timezone.now() + timedelta(days=1))
        self.assertFalse(notification.is_between_dates())

    def test_queue_between_start_and_end_date(self):
        notification = Notification.objects.get(pk=5)
        self.assertTrue(notification.is_between_dates())
    
    def test_add_user_message_success(self):
        notification = Notification.objects.get(pk=5)
        self.assertFalse(Message.objects.all().count())
        notification.add_user_message(User.objects.get(pk=1))
        self.assertTrue(Message.objects.all().count())

    def test_already_exists_true(self):
        user = User.objects.get(pk=1)
        notification = Notification.objects.get(pk=5)
        self.assertFalse(Message.objects.all().count())
        notification.add_user_message(user)
        self.assertTrue(notification.already_exists(user))
    
    def test_already_exists_false(self):
        notification = Notification.objects.get(pk=5)
        self.assertFalse(notification.already_exists(User.objects.get(pk=1)))

    def test_save_accepted(self):
        user = User.objects.get(pk=1)
        notification = Notification.objects.get(pk=5)
        notification.save_accepted(user, Site.objects.get(pk=1))
        self.assertIn('accepted', notification.meta.keys())
        self.assertIn(user.username, notification.meta['accepted'][Site.objects.get(pk=1).domain].keys())

    def test_save_decline(self):
        user = User.objects.get(pk=1)
        notification = Notification.objects.get(pk=5)
        notification.save_declined(user, Site.objects.get(pk=1))
        self.assertIn('declined', notification.meta.keys())
        self.assertIn(user.username, notification.meta['declined'][Site.objects.get(pk=1).domain].keys())
        
    def test_save_user_acknowledgement(self):
        user = User.objects.get(pk=1)
        notification = Notification.objects.get(pk=2)
        notification.add_user_message(user)
        notification.refresh_from_db()
        notification.save_user_acknowledgement(user, Site.objects.get(pk=1), True)
        self.assertIn('accepted', notification.meta.keys())
        self.assertIn(user.username, notification.meta['accepted'][Site.objects.get(pk=1).domain].keys())

        




        
