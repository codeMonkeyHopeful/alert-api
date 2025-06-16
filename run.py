from app import create_app
import os
from dotenv import load_dotenv

load_dotenv()

app = create_app()

if __name__ == "__main__":

    port = os.environ.get("SERVER_PORT", 5000)
    host = os.environ.get("HOST", 5000)

    for key, value in app.config.items():
        print(f"{key} = {value}")

    app.run(host="0.0.0.0", port=port)
