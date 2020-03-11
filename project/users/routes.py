#################
#### imports ####
#################
from flask import render_template, request, redirect, url_for, flash, escape, current_app, copy_current_request_context
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, current_user, login_required, logout_user
from flask_mail import Message
from threading import Thread
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature
from datetime import datetime

from . import users_blueprint
from .forms import RegistrationForm, LoginForm, EmailForm, PasswordForm
from project.models import User
from project import database, mail


########################
### helper functions ###
########################

def generate_confirmation_email(user_email):
    confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    confirm_url = url_for('users.confirm_email',
                          token=confirm_serializer.dumps(user_email, salt='email-confirmation-salt'),
                          _external=True)

    return Message(subject='Flask Stock Portfolio App - Confirm Your Email Address',
                   html=render_template('users/email_confirmation.html', confirm_url=confirm_url),
                   recipients=[user_email])


def generate_password_reset_email(user_email):
    password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    password_reset_url = url_for('users.process_password_reset_token',
                                 token=password_reset_serializer.dumps(user_email, salt='password-reset-salt'),
                                 _external=True)

    return Message(subject='Flask Stock Portfolio App - Password Reset Requested',
                   html=render_template('users/email_password_reset.html', password_reset_url=password_reset_url),
                   recipients=[user_email])


################
#### routes ####
################

@users_blueprint.route('/user_profile')
@login_required
def user_profile():
    return render_template('users/user_profile.html')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_user = User(form.email.data, form.password.data)
                database.session.add(new_user)
                database.session.commit()
                flash('Thanks for registering, {}! Please check your email to confirm your email address.'.format(new_user.email))
                current_app.logger.info(f"Registered new user: ({form.email.data})!")

                @copy_current_request_context
                def send_email(email_message):
                    with current_app.app_context():
                        mail.send(email_message)

                # Send an email confirming the new registration
                message = generate_confirmation_email(form.email.data)
                email_thread = Thread(target=send_email, args=[message])
                email_thread.start()

                return redirect(url_for('users.login'))
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
        return redirect(url_for('users.user_profile'))

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
                return redirect(url_for('users.user_profile'))

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


@users_blueprint.route('/confirm/<token>')
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
    except BadSignature as e:
        flash(f'The confirmation link is invalid or has expired.', 'error')
        return redirect(url_for('users.login'))

    user = User.query.filter_by(email=email).first()

    if user.email_confirmed:
        flash('Account already confirmed. Please login.', 'info')
    else:
        user.email_confirmed = True
        user.email_confirmed_on = datetime.now()
        database.session.add(user)
        database.session.commit()
        flash('Thank you for confirming your email address!', 'success')

    return redirect(url_for('stocks.index'))


@users_blueprint.route('/password_reset_via_email', methods=['GET', 'POST'])
def password_reset_via_email():
    form = EmailForm()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first_or_404()
        except:
            flash('Error! Invalid email address!', 'error')
            return render_template('users/password_reset_via_email.html', form=form)

        if user.email_confirmed:
            @copy_current_request_context
            def send_email(email_message):
                with current_app.app_context():
                    mail.send(email_message)

            # Send an email confirming the new registration
            message = generate_password_reset_email(form.email.data)
            email_thread = Thread(target=send_email, args=[message])
            email_thread.start()

            flash('Please check your email for a password reset link.', 'success')
        else:
            flash('Your email address must be confirmed before attempting a password reset.', 'error')
        return redirect(url_for('users.login'))

    return render_template('users/password_reset_via_email.html', form=form)


@users_blueprint.route('/password_reset_via_token/<token>', methods=['GET', 'POST'])
def process_password_reset_token(token):
    try:
        password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = password_reset_serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except BadSignature as e:
        flash('The password reset link is invalid or has expired.', 'error')
        return redirect(url_for('users.login'))

    form = PasswordForm()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=email).first()
        except:
            flash('Invalid email address!', 'error')
            return redirect(url_for('users.login'))

        user.set_password(form.password.data)
        database.session.add(user)
        database.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('users.login'))

    return render_template('users/reset_password_with_token.html', form=form)


@users_blueprint.route('/change_password', methods=['GET', 'POST'])
def change_password():
    return '<h1>Page Is Under Construction</h1>'


@users_blueprint.route('/resend_email_confirmation')
def resend_email_confirmation():
    return '<h1>Page Is Under Construction</h1>'
