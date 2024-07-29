import os


class RabbitMQParams:
    # RabbitMQ URLs
    LOGS_RABBITMQ = {
        'HOST': os.getenv('LOGS_RABBITMQ_HOST'),
        'USERNAME': os.getenv('LOGS_RABBITMQ_USERNAME'),
        'PASSWORD': os.getenv('LOGS_RABBITMQ_PASSWORD'),
        'EXCHANGE': os.getenv('LOGS_RABBITMQ_EXCHANGE'),
        'QUEUE_NAME': os.getenv('LOGS_RABBITMQ_QUEUE_NAME'),
        'EXCHANGE_TYPE': os.getenv('LOGS_RABBITMQ_EXCHANGE_TYPE'),
    }

    RULES_CHANGE_RABBITMQ = {
        'HOST': os.getenv('RULES_RABBITMQ_HOST'),
        'USERNAME': os.getenv('RULES_RABBITMQ_USERNAME'),
        'PASSWORD': os.getenv('RULES_RABBITMQ_PASSWORD'),
        'EXCHANGE': os.getenv('RULES_RABBITMQ_EXCHANGE'),
        'QUEUE_NAME': os.getenv('RULES_RABBITMQ_QUEUE_NAME'),
        'EXCHANGE_TYPE': os.getenv('RULES_RABBITMQ_EXCHANGE_TYPE'),
        'ROUTING_KEY': os.getenv('RULES_RABBITMQ_ROUTING_KEY'),
    }

    NOTIFICATIONS_RABBITMQ = {
        'HOST': os.getenv('NOTIFICATIONS_RABBITMQ_HOST'),
        'USERNAME': os.getenv('NOTIFICATIONS_RABBITMQ_USERNAME'),
        'PASSWORD': os.getenv('NOTIFICATIONS_RABBITMQ_PASSWORD'),
        'EXCHANGE': os.getenv('NOTIFICATIONS_RABBITMQ_EXCHANGE'),
        'ROUTING_KEY': os.getenv('NOTIFICATIONS_RABBITMQ_ROUTING_KEY'),
        'EXCHANGE_TYPE': os.getenv('NOTIFICATIONS_RABBITMQ_EXCHANGE_TYPE'),
        'QUEUE_NAME': os.getenv('NOTIFICATIONS_RABBITMQ_QUEUE_NAME'),
    }
