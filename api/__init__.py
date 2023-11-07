import os

from flask import Flask
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv

load_dotenv()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    print(app.instance_path)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    print(os.getenv("MONGO_HOST"))
    app.config['MONGODB_SETTINGS'] = {
        "db": "calorie_compass",
        "host": os.getenv("MONGO_HOST"),
        "port": 27017,
        "username": os.getenv("MONGO_USERNAME"),
        "password": os.getenv("MONGO_PASSWORD") 
    }
    db = MongoEngine()
    db.init_app(app)
    from api import user
    app.register_blueprint(user.user_blueprint)

    return app
