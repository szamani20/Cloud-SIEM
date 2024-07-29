from flask import Flask
from .config import Config
from .db import init_db
from .auth.routes import auth_bp
from .main.routes import main_bp

from flask_jwt_extended import JWTManager

from .utils.rabbitmq.producer import RabbitMQProducer


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)

    JWTManager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # Initialize RabbitMQProducer and store it in the app context
    app.rabbitmq_producer = RabbitMQProducer(rabbitmq_params=Config.RABBITMQ_PARAMS)

    return app
