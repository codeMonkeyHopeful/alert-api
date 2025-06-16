from app import create_app
import os
from dotenv import load_dotenv

load_dotenv()

app = create_app()

if __name__ == "__main__":

    port = os.environ.get("SERVER_PORT", 5000)
    host = os.environ.get("HOST", "0.0.0.0")

    app.logger.info(f"Starting server on {host}:{port}")

    app.run(host=host, port=port)
