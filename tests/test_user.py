import json


def register_user(client, username, password):
    data = {
        "username": username,
        "password": password,
        "repeat_password": password
    }
    response = client.post('/auth/register', data=json.dumps(data), content_type='application/json')
    return response


def login_user(client, username, password):
    data = {
        "username": username,
        "password": password
    }
    response = client.post('/auth/login', data=json.dumps(data), content_type='application/json')
    return response


def test_register_user(client):
    username = "testuser"
    password = "Password123!"
    response = register_user(client, username, password)
    assert response.status_code == 200
    assert 'username' in response.data.decode()


def test_register_existing_user(client):
    username = "testuser"
    password = "Password123!"
    register_user(client, username, password)
    response = register_user(client, username, password)
    assert response.status_code == 400
    assert 'User testuser is already registered' in response.data.decode()


def test_register_missing_username(client):
    password = "Password123!"
    data = {"password": password}
    response = client.post('/auth/register', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 422


def test_register_missing_password(client):
    username = "testuser"
    data = {"username": username}
    response = client.post('/auth/register', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 422


def test_login_user(client):
    username = "testuser"
    password = "Password123!"
    register_user(client, username, password)
    response = login_user(client, username, password)
    assert response.status_code == 200
    assert 'username' in response.data.decode()


def test_login_incorrect_username(client):
    username = "testuser"
    password = "Password123!"
    register_user(client, username, password)
    response = login_user(client, "nonexistentuser", password)
    assert response.status_code == 400
    assert 'Incorrect username' in response.data.decode()


def test_login_incorrect_password(client):
    username = "testuser"
    password = "Password123!"
    register_user(client, username, password)
    response = login_user(client, username, "incorrectpassword")
    assert response.status_code == 400
    assert 'Incorrect password' in response.data.decode()
    with client.session_transaction() as sess:
        assert 'user_id' not in sess


def test_logout(client):
    username = "testuser"
    password = "Password123!"
    register_user(client, username, password)
    login_response = login_user(client, username, password)
    assert login_response.status_code == 200

    response = client.post('/auth/logout')
    assert response.status_code == 200
    assert 'Successfully logged out' in response.data.decode()

    with client.session_transaction() as sess:
        assert 'user_id' not in sess

def test_delete(client):
    username = "testuser"
    password = "Password123!"
    register_user(client, username, password)
    login_response = login_user(client, username, password)
    assert login_response.status_code == 200

    response = client.post('/auth/delete')
    assert response.status_code == 200
    assert 'Successfully deleted' in response.data.decode()

    with client.session_transaction() as sess:
        assert 'user_id' not in sess

    login_response = login_user(client, username, password)
    assert login_response.status_code == 400
