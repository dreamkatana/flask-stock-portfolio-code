#################
#### imports ####
#################
from . import users_blueprint
from flask import render_template, request, redirect, url_for, flash, escape, current_app
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, current_user, login_required, logout_user
from .forms import RegistrationForm, LoginForm
from project.models import User
from project import database


################
#### routes ####
################

@users_blueprint.route('/users/<email>')
def user_profile(email):
    return render_template('users/user_profile.html', email=email)


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_user = User(form.email.data, form.password.data)
                database.session.add(new_user)
                database.session.commit()
                flash('Thanks for registering, {}!'.format(new_user.email))
                current_app.logger.info(f"Registered new user: ({form.email.data})!")
                return redirect(url_for('users.user_profile', email=form.email.data))
            except IntegrityError:
                database.session.rollback()
                flash('ERROR! Email ({}) already exists.'.format(form.email.data), 'error')
        else:
            flash(f"Error in form data!")

    return render_template('users/register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # If the User is already logged in, don't allow them to try to log in again
    if current_user.is_authenticated:
        flash('Already logged in!  Redirecting to your User Profile page...')
        return redirect(url_for('users.user_profile', email=current_user.email))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.is_password_correct(form.password.data):
                # User's credentials have been validated, so log them in
                user.authenticated = True
                database.session.add(user)
                database.session.commit()
                login_user(user, remember=form.remember_me.data)
                flash('Thanks for logging in, {}!'.format(current_user.email))
                return redirect(url_for('users.user_profile', email=form.email.data))

        flash('ERROR! Incorrect login credentials.')
    return render_template('users/login.html', form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    current_user.authenticated = False
    database.session.add(current_user)
    database.session.commit()
    logout_user()
    flash('Goodbye!')
    return redirect(url_for('stocks.index'))
