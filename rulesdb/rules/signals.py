import json

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from utils.rabbitmq.producer import RabbitMQProducer
from .models import Rule
from django.conf import settings


@receiver(post_save, sender=Rule)
def rule_post_save(sender, instance, created, **kwargs):
    """
    Upon creation of a new rule, or modification of an existing one, this signal method
    is invoked. This method utilizes a RabbitMQ producer that broadcasts the details of this change to
    rules to its subscribers. The subscribers can decide what to do with this new information.
    """
    rabbitmq_producer = RabbitMQProducer(settings.RULES_RABBITMQ)

    message = {
        'created': created  # Whether this is a newly created rule, or a modification of an existing one
    }

    # Store all the fields of the rule in the message body to be broadcasted
    for field in instance._meta.get_fields():
        field_value = getattr(instance, field.name)
        if field_value is not None:
            if field.is_relation:
                message[field.name+'_id'] = field_value.pk
            elif 'time' in field.name:
                message[field.name] = field_value.isoformat()
            else:
                message[field.name] = field_value

    rabbitmq_producer.publish_message(json.dumps(message))


@receiver(post_delete, sender=Rule)
def rule_post_delete(sender, instance, **kwargs):
    """
    Upon deletion of a rule, this signal method
    is invoked. This method utilizes a RabbitMQ producer that broadcasts the details of this change to
    rule to its subscribers. The subscribers can decide what to do with this new information.
    """
    rabbitmq_producer = RabbitMQProducer(settings.RULES_RABBITMQ)

    message = {
        'deleted': True,
    }

    # Store all the fields of the rule in the message body to be broadcasted
    for field in instance._meta.get_fields():
        field_value = getattr(instance, field.name)
        if field_value is not None:
            if field.is_relation:
                message[field.name+'_id'] = field_value.pk
            elif 'time' in field.name:
                message[field.name] = field_value.isoformat()
            else:
                message[field.name] = field_value

    rabbitmq_producer.publish_message(json.dumps(message))
