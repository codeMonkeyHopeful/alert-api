from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()


def add_all_blueprints(app):
    from .routes.health_check import health_check

    api_prefix = os.environ.get("API_PREFIX", "/api")

    app.register_blueprint(health_check, url_prefix=api_prefix)
    # Add other blueprints here as needed
    # from .routes.another_route import another_route
    # app.register_blueprint(another_route)


def create_app():

    app = Flask(__name__)

    # app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "default-secret")

    add_all_blueprints(app)

    return app
