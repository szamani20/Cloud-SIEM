from django.db import models
from django.utils import timezone

from organization.models import Organization


class NotificationSubscription(models.Model):
    """
    A notification subscription is an AWS SNS Topic ARN that represents a SNS Topic in OUR AWS cloud
    that is supposed to be used to send real-time (and non-real-time) notifications upon noticing
    unwanted behavior in customers' AWS cloud
    """
    notification_subscription_id = models.AutoField(primary_key=True)

    organization = models.ForeignKey(Organization, models.DO_NOTHING)

    topic_arn = models.CharField(max_length=255)

    notification_types = [
        ('EMAIL', 'Email'),
        ('SMS', 'SMS'),
        ('OTHER', 'Other'),
    ]
    notification_type = models.CharField(max_length=100, choices=notification_types, blank=True, null=True)

    create_time = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        # managed = False
        db_table = 'notification_subscriptions'

    def __str__(self):
        return f"{self.notification_subscription_id} - {self.organization} - {self.create_time}"


class Notification(models.Model):
    """
    A notification instance represents a sent notification to customers. When a notification is sent to a
    customer, a new instance of this class must be registered to DB
    """
    notification_id = models.AutoField(primary_key=True)

    organization = models.ForeignKey(Organization, models.DO_NOTHING)
    notification_subscription = models.ForeignKey(NotificationSubscription, models.DO_NOTHING)

    notification_content = models.TextField()

    create_time = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        # managed = False
        db_table = 'notifications'

    def __str__(self):
        return f"{self.notification_id} - {self.organization} - {self.create_time}"
