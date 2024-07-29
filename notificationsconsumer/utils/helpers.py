import json


def extract_organization_from_message(message):
    """
    This helper method is used to extract the organization_id and the notification main message body from
    a RabbitMQ message generated by NOTIFICATIONS_RABBITMQ Producer
    :param message: Json string containing message and organization_id
    :type message: str
    :return:
    :rtype:
    """
    message = json.loads(message)
    notification = message['message']
    organization_id = message['organization_id']
    return notification, organization_id