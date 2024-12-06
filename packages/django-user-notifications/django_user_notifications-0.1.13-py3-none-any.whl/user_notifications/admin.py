from django.contrib import admin
from user_notifications.models import Notification

# Register your models here.
###############
# MODEL ADMINS
###############
class NotificationAdmin(admin.ModelAdmin):
    fields = ('active', 'deliver_once', 'name', 'sites', 'display_type', 'message', 'rules', 'meta')
    list_display = ('pk', 'name', 'active', 'deliver_once', 'display_type')


admin.site.register(Notification, NotificationAdmin)