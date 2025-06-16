from flask import Flask
from dotenv import load_dotenv
import os
import sys
import importlib

load_dotenv()


# Make sure Python can find the routes/ package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)


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
            print(f"⚠️ No get_blueprint() in {module_name}")


def create_app():

    app = Flask(__name__)

    # app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "default-secret")

    # add_all_blueprints(app)
    register_blueprints(app)

    return app
