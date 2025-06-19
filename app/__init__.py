from flask import Flask, jsonify
from dotenv import load_dotenv
import os
import sys
import importlib
import logging
from datetime import timedelta
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import JWTExtendedException

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
    log_level_name = app.config.get("LOG_LEVEL", "WARNING").upper()
    log_level = getattr(logging, log_level_name, logging.WARNING)

    app.logger.setLevel(log_level)

    # Add a console handler if none exist
    if not app.logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        )
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)

    app.logger.info(f"Logging configured at {log_level_name} level")


def get_env(app):
    # Choose config based on FLASK_ENV
    env = os.getenv("FLASK_ENV", "production").lower()

    if env == "development":
        from .config import DevelopmentConfig

        app.config.from_object(DevelopmentConfig)
    elif env == "testing":
        from .config import TestingConfig

        app.config.from_object(TestingConfig)
    else:
        from .config import ProductionConfig

        app.config.from_object(ProductionConfig)

    app.logger.info(f"Environment set to {env.upper()}")


def create_app():

    app = Flask(__name__)

    jwt_secret = os.getenv("JWT_SECRET_KEY")
    if not jwt_secret:
        raise RuntimeError("JWT_SECRET_KEY is not set in environment variables.")
    app.config["JWT_SECRET_KEY"] = jwt_secret
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    jwt = JWTManager(app)

    @app.errorhandler(JWTExtendedException)
    def handle_jwt_errors(e):
        return jsonify({"msg": str(e)}), 401

    get_env(app)  # Load environment-specific configuration

    setup_logging(app)
    # app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "default-secret")

    register_blueprints(app)
    return app
