from flask import Blueprint, jsonify

bp = Blueprint("main", __name__)

route_prefix = ""


@bp.route("/", methods=["GET"])
def main():

    return jsonify({"status": "ok"})


def get_blueprint():
    return bp, route_prefix
    """
    Returns the health check response.
    """
    return jsonify({"status": "ok"}), 200
