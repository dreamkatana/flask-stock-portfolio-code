#################
#### imports ####
#################
from . import users_blueprint
from flask import render_template, request, redirect, url_for, flash, escape, current_app
from sqlalchemy.exc import IntegrityError
from .forms import RegistrationForm
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
