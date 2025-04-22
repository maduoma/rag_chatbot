from flask import Flask
from app.ui import routes
import os

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(base_dir, "templates")
    static_dir = os.path.join(base_dir, "static")
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    # Set a secure secret key for session management
    app.secret_key = os.environ.get("SECRET_KEY", "change_this_secret_key")
    routes.init_routes(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
else:
    app = create_app()
