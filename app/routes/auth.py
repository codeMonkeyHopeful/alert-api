from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    create_refresh_token,
)
import bcrypt

bp = Blueprint("auth", __name__)

route_prefix = "/auth"


def hash_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password.encode(), bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode()
    return bcrypt.checkpw(plain_text_password.encode(), hashed_password)


# Fake user for demonstration purposes
db_password = hash_password("test")
# This is how it would be stored in a database
fake_user = {"username": "test", "password": db_password, "id": 1}


@bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    # TODO: Implement real authentication logic

    # Call to the DB here to get the user information
    # need to test if user exists and ony then proceed.

    # Simulate DB lookup
    if username != fake_user["username"]:
        return jsonify({"msg": "Unauthorized"}), 401

    # Check password using bcrypt
    if not check_password(password, fake_user["password"]):
        return jsonify({"msg": "Unauthorized"}), 401

    access_token = create_access_token(identity=fake_user["id"])
    refresh_token = create_refresh_token(identity=fake_user["id"])
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        user_id = get_jwt_identity()
        new_token = create_access_token(identity=user_id)
        return jsonify(access_token=new_token)
    except Exception as e:
        return jsonify({"msg": str(e)}), 401


def get_blueprint():
    return bp, route_prefix
