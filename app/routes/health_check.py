from flask import Blueprint, jsonify

health_check = Blueprint("main", __name__)


@health_check.route("/api/health", methods=["GET"])
def health():

    return jsonify({"status": "ok"})
