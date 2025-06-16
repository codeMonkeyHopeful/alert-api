from flask import Blueprint, jsonify

health_check = Blueprint("main", __name__)

route_prefix = "/health"


@health_check.route("/", methods=["GET"])
def health():

    return jsonify({"status": "ok"})


def return_routes():
    return health_check, route_prefix
    """
    Returns the health check response.
    """
    return jsonify({"status": "ok"}), 200
