from django.contrib import admin

from notifications.models import Notification, NotificationSubscription


@admin.register(NotificationSubscription)
class NotificationSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('notification_subscription_id', 'organization', 'notification_type', 'create_time')
    list_filter = ('organization', 'notification_type', 'create_time')
    search_fields = ('organization__organization_name', 'organization__organization_account_id', 'topic_arn')
    ordering = ('-create_time',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_id', 'organization', 'notification_subscription', 'create_time')
    list_filter = ('organization', 'notification_subscription', 'create_time')
    search_fields = ('organization__organization_name', 'organization__organization_account_id', 'notification_content')
    ordering = ('-create_time',)
