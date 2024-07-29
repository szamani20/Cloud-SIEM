import json

from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.db.models import User
# from app.utils.rabbitmq.producer import RabbitMQProducer

main_bp = Blueprint('main', __name__, url_prefix='/main')


@main_bp.route('/dummy', methods=['GET'])
@jwt_required()
def dummy_endpoint():
    # current_app.rabbitmq_producer = None
    return jsonify({"msg": "This is a dummy endpoint"}), 200


@main_bp.route('/send_logs', methods=['POST'])
@jwt_required()
def send_logs():
    """
    The purpose of this endpoint is to simply get a log from AWS client, attach a
    username (organization name) to it, and then send it on a rabbitmq fanout exchange.
    The consumers of the fanout exchange are for logs retention and real-time notification purposes
    Specifically, logs retention is responsible for permanently storing the logs and
    real-time notification is responsible for determining whether a notification is required or not
    and if so, start the process for sending the notification.
    Both of these are their own separate applications where they have a consumer subscribed to this
    fanout exchange.
    """
    data = request.get_json()
    user = User.query.get(get_jwt_identity()).username
    data['organization'] = user
    try:
        message, status_code = current_app.rabbitmq_producer.publish_message(message=json.dumps(data))
        return message, status_code
    except Exception as e:
        print(e)
        return 'Error', 500
        # current_app.rabbitmq_producer = RabbitMQProducer(rabbitmq_params=current_app.config.RABBITMQ_PARAMS)
        # message, status_code = current_app.rabbitmq_producer.publish_message(message=json.dumps(data))
        # return message, status_code
