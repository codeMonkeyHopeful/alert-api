from flask import Blueprint, jsonify
import datetime

bp = Blueprint("health", __name__)

route_prefix = "/health"


@bp.route("/", methods=["GET"])
def health():

    return jsonify(
        {
            "status": "ok",
            "current_time": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
    )


def get_blueprint():
    return bp, route_prefix
