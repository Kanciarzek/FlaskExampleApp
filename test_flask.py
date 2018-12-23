import tempfile
import pytest
from app import app
from db import init_db


# Dekorator pytest.fixture powoduje, że wynik działania tej funkcji zostanie zaaplikowany jako argument pozostałych
# funkcji, które przyjmują argument o tej nazwie - konkretnie wynik dziaałania tej funkcji zostanie wstawiony jako
# argument client funkcji test_return_status oraz test_return_message
@pytest.fixture
def client():
    return app.test_client()


# Tworzymy osobny fixture, który zwraca nam klienta, który ma dostęp do bazy danych (nie każdy test z niej korzysta)
@pytest.fixture
def client_with_db():
    db, app.config['DATABASE'] = tempfile.mkstemp()  # Tworzona jest baza danych w folderze tymczasowym o losowej nazwie
    with app.app_context():
        init_db()
    return app.test_client()


# Dla każdego testu powyższe metody są wywoływane osobno - w szczególności każdy test wykorzystujący bazę danych otrzyma
# bazę bez żadnych rekordów


def test_return_status(client):
    result = client.get('/hello_not_found/')
    assert result.status_code == 404


def test_return_message(client):
    result = client.get('/')
    assert b'Hello World' in result.data


def test_empty_db(client_with_db):
    result = client_with_db.get('/blog')
    assert b'Posts: 0' in result.data
