import os


class PostgreSQLParams:
    # PostgreSQL URLs
    LOGS_POSTGRES_PARAMS = {
        'HOST': os.getenv("LOGS_POSTGRES_HOST"),
        'USER': os.getenv("LOGS_POSTGRES_USER"),
        'PASSWORD': os.getenv("LOGS_POSTGRES_PASSWORD"),
        'DATABASE': os.getenv("LOGS_POSTGRES_DATABASE"),
        'PORT': os.getenv("LOGS_POSTGRES_PORT"),
    }
