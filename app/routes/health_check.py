from flask import Blueprint, jsonify

health_check = Blueprint("health", __name__)

route_prefix = "/health"


@health_check.route("/", methods=["GET"])
def health():

    return jsonify({"status": "ok"})


def get_blueprint():
    return health_check, route_prefix
