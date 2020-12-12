import click
from . import admin_blueprint
from project import database
from project.models import User
from flask import render_template, current_app, abort
from flask_login import login_required, current_user


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


###########################
#### request callbacks ####
###########################

@admin_blueprint.before_request
@login_required
def admin_before_request():
    if current_user.user_type != 'Admin':
        current_app.logger.info(f'User {current_user.id} attempted to access ADMIN pages!')
        abort(403)


################
#### routes ####
################

@admin_blueprint.route('/users')
def admin_list_users():
    users = User.query.order_by(User.id).all()
    return render_template('admin/users.html', users=users)
