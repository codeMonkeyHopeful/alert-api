from flask import Blueprint, jsonify
import datetime

bp = Blueprint("main", __name__)

route_prefix = ""


@bp.route("/", methods=["GET"])
def main():

    return jsonify(
        {
            "status": "ok",
            "current_time": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
    )


def get_blueprint():
    return bp, route_prefix
