from flask import Flask
from dotenv import load_dotenv
import os
import sys
import importlib
import logging

load_dotenv()

# Make sure Python can find the routes/ package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def register_blueprints(app, routes_dir=None, api_prefix="/api"):
    if routes_dir is None:
        # Automatically find app/routes/ relative to this file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        routes_dir = os.path.join(base_dir, "routes")

    for filename in os.listdir(routes_dir):
        if filename.startswith("_") or not filename.endswith(".py"):
            continue

        module_name = f"app.routes.{filename[:-3]}"  # e.g., app.routes.users
        module = importlib.import_module(module_name)

        print(f"🔍 Registering blueprint from {module_name}")
        print(f"Module: {module}")

        if hasattr(module, "get_blueprint"):
            blueprint, prefix = module.get_blueprint()
            app.register_blueprint(blueprint, url_prefix=f"{api_prefix}{prefix}")
        else:
            print(f"No get_blueprint() in {module_name}")


def setup_logging(app):
    flask_env = os.environ.get("FLASK_ENV", "production").lower()

    if flask_env == "production":
        log_level = logging.CRITICAL + 1
    else:
        log_level_name = os.environ.get("LOG_LEVEL", "DEBUG").upper()
        log_level = getattr(logging, log_level_name, logging.DEBUG)

    app.logger.setLevel(log_level)

    # Add a StreamHandler if no handlers exist
    if not app.logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        )
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)

    app.logger.info(
        f"Logging set to {logging.getLevelName(log_level)} for FLASK_ENV={flask_env}"
    )


def create_app():

    app = Flask(__name__)

    # Load configuration from environment variables or a .env file
    setup_logging(app)
    # app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "default-secret")

    register_blueprints(app)
    return app
