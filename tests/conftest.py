import mongomock
import pytest
from flask import Flask
from mongoengine import connect


@pytest.fixture(scope="module")
def app():
    a = Flask(__name__)
    a.config['SECRET_KEY'] = "secret"
    a.config['TESTING'] = True
    a.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    a.config['SECRET_KEY'] = "something unique"

    # Use mongomock for testing
    a.config['MONGODB_SETTINGS'] = {
        'db': 'test_db',
        'host': 'mongodb://localhost',
    }
    connect('test_db', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient)
    from api import user
    a.register_blueprint(user.user_blueprint)

    return a


@pytest.fixture(scope="module")
def client(app):
    return app.test_client()
