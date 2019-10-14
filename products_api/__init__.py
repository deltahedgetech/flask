from flask import Flask
from products_api.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from products_api.main.routes import main
    app.register_blueprint(main)

    return app
