import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 86400)))

    RABBITMQ_PARAMS = {
        'HOST': os.getenv('RABBITMQ_HOST'),
        'USERNAME': os.getenv('RABBITMQ_USERNAME'),
        'PASSWORD': os.getenv('RABBITMQ_PASSWORD'),
        'EXCHANGE': os.getenv('RABBITMQ_EXCHANGE'),
        'EXCHANGE_TYPE': os.getenv('RABBITMQ_EXCHANGE_TYPE')
    }
