import click

from app.extensions import db


def initialize_cli(app):
    @app.cli.command()
    def init_db():
        """Initialize the database."""
        click.echo('Initializing the db')
        db.create_all()
