import json


def extract_organization_from_message(message):
    """
    This helper method is used to extract the organization name from a RabbitMQ message generated by logs_fanout_exchange Producer
    :param message: Json string containing organization name and the rest of the AWS log
    :type message: str
    :return:
    :rtype:
    """
    message = json.loads(message)
    organization = message['organization']
    return message, organization
