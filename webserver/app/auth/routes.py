from flask import Blueprint, request, jsonify
from app.db.models import User
from app.db import db
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    This endpoint is used to register a webserver user to a local SQLite database.
    Users of the webserver are limited as the endpoints are only called by a Lambda within customers' AWS
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    This endpoint is used to authenticate a webserver user to a local SQLite database.
    Users of the webserver are limited as the endpoints are only called by a Lambda within customers' AWS
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify(access_token=new_access_token), 200


@auth_bp.route('/who_am_i', methods=['GET'])
@jwt_required()
def who_am_i():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify(username=user.username), 200
