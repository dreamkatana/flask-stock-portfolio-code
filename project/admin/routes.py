import click
from . import admin_blueprint
from project import database
from project.models import User


######################
#### cli commands ####
######################

@admin_blueprint.cli.command('create_admin_user')
@click.argument('email')
@click.argument('password')
def create(email, password):
    """Create a new admin user and add it to the database."""
    admin_user = User(email, password, user_type='Admin')
    database.session.add(admin_user)
    database.session.commit()
    click.echo(f'Created new admin user ({email})!')
