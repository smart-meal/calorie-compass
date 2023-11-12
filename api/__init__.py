from datetime import timedelta

from flask import Flask
from flask_mongoengine import MongoEngine

from api import config


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=config.SECRET_KEY,
    )
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = False

    app.config['MONGODB_SETTINGS'] = {
        "db": config.MONGO_DB_NAME,
        "host": config.MONGO_HOST,
        "port": config.MONGO_PORT,
        "username": config.MONGO_USERNAME,
        "password": config.MONGO_PASSWORD,
    }
    db = MongoEngine()
    db.init_app(app)
    from api import user
    app.register_blueprint(user.user_blueprint)

    return app
