import click

from app.extensions import db
from app.models.initializers.users import add_initial_roles_to_database


def initialize_cli(app):
    @app.cli.command()
    def init_db():
        """Initialize the database."""
        click.echo('Initializing the db')
        db.create_all()

    @app.cli.command()
    def clear_db():
        """Initialize the database."""
        click.echo('Clearing the db')
        db.drop_all()
        click.echo('Initializing the db')
        db.create_all()

    @app.cli.command()
    def insert_sample_data():
        """Initialize the database."""
        add_initial_roles_to_database()
