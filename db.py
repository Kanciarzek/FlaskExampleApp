import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


def init_app(app):
    app.teardown_appcontext(close_db)  # Dziękki temu przy zakończeniu pracy z aplikacją połączenie z bazą danych
    # będzie zamykane
    app.cli.add_command(init_db_command)  # Dzieki temu możemy zainicjalizować naszą bazę za pomocą flask init-db


# Zwraca obiekt reprezentujący bazę danych
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE']
        )
        g.db.row_factory = sqlite3.Row
    return g.db


# Zamyka połączenie z bazą danych
def close_db(e=0):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# Funkcją generująca naszą tabelę (wysyłająca zapytanie z pliku schema.sql)
def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
