from flask import Flask
from app.routes import routes
from .routes import routes

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.secret_key = '976f64429ca2f7160b26c278c77d6a2b705fa06da94fc5fd93727e4cb97fb831'
    app.register_blueprint(routes)

    return app
