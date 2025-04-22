from flask import Flask
from app.ui.routes import init_routes
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

init_routes(app)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
