import os


class RabbitMQParams:
    # RabbitMQ URLs
    LOGS_RABBITMQ = {
        'HOST': os.getenv('LOGS_RABBITMQ_HOST'),
        'USERNAME': os.getenv('LOGS_RABBITMQ_USERNAME'),
        'PASSWORD': os.getenv('LOGS_RABBITMQ_PASSWORD'),
        'EXCHANGE': os.getenv('LOGS_RABBITMQ_EXCHANGE'),
        'EXCHANGE_TYPE': os.getenv('LOGS_RABBITMQ_EXCHANGE_TYPE'),
        'QUEUE_NAME': os.getenv('LOGS_RABBITMQ_QUEUE_NAME'),
    }
