import os


class PostgreSQLParams:
    # RabbitMQ URLs
    NOTIFICATION_SUBSCRIPTION_POSTGRES = {
        'HOST': os.getenv("RULES_POSTGRES_HOST"),
        'USER': os.getenv("RULES_POSTGRES_USER"),
        'PASSWORD': os.getenv("RULES_POSTGRES_PASSWORD"),
        'DATABASE': os.getenv("RULES_POSTGRES_DATABASE"),
        'PORT': os.getenv("RULES_POSTGRES_PORT"),
    }