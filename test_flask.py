import tempfile
import pytest
from app import app
from db import init_db


@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def client_with_db():
    db, app.config['DATABASE'] = tempfile.mkstemp()
    with app.app_context():
        init_db()
    return app.test_client()


def test_return_status(client):
    result = client.get('/hello_not_found/')
    assert result.status_code == 404


def test_return_message(client):
    result = client.get('/')
    assert b'Hello World' in result.data


def test_empty_db(client_with_db):
    result = client_with_db.get('/blog')
    assert b'Posts: 0' in result.data
