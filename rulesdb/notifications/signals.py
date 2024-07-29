import json

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from utils.rabbitmq.producer import RabbitMQProducer
from .models import NotificationSubscription
from django.conf import settings


@receiver(post_save, sender=NotificationSubscription)
def notification_subscription_post_save(sender, instance, created, **kwargs):
    """
    Upon creation of a new notification subscription, or modification of an existing one, this signal method
    is invoked. This method utilizes a RabbitMQ producer that broadcasts the details of this change to
    notification subscription to its subscribers. The subscribers can decide what to do with this new information.
    """
    rabbitmq_producer = RabbitMQProducer(settings.NOTIFICATIONS_SUBSCRIPTION_RABBITMQ)

    message = {
        'created': created,  # Whether this is a newly created notification subscription, or a modification of an existing one
        'notification_subscription_id': instance.notification_subscription_id,  # The id of the notification subscription
        'organization_id': instance.organization.organization_id,
        # The organization_id associated with the notification subscription
        'topic_arn': instance.topic_arn,  # The topic ARN of the notification subscription
    }

    rabbitmq_producer.publish_message(json.dumps(message))


@receiver(post_delete, sender=NotificationSubscription)
def notification_subscription_post_delete(sender, instance, **kwargs):
    """
    Upon deletion of a notification subscription, this signal method
    is invoked. This method utilizes a RabbitMQ producer that broadcasts the details of this change to
    notification subscription to its subscribers. The subscribers can decide what to do with this new information.
    """
    rabbitmq_producer = RabbitMQProducer(settings.NOTIFICATIONS_SUBSCRIPTION_RABBITMQ)

    message = {
        'deleted': True,
        'notification_subscription_id': instance.notification_subscription_id,  # The id of the notification subscription
        'organization_id': instance.organization.organization_id,
        # The organization_id associated with the notification subscription
        'topic_arn': instance.topic_arn,  # The topic ARN of the notification subscription
    }

    rabbitmq_producer.publish_message(json.dumps(message))
