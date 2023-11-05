import os

from flask import Flask
from flask_mongoengine import MongoEngine


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
    app.config['MONGODB_SETTINGS'] = {
        "db": "calorie_compass",
        "host": "mongodb://127.0.0.1",
        "port": 27017,
        "username": "root",
        "password": "password"  # TODO move these into environment variable
    }
    db = MongoEngine()
    db.init_app(app)
    from . import auth
    app.register_blueprint(auth.bp)

    return app
