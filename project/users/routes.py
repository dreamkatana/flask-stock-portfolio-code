#################
#### imports ####
#################
from . import users_blueprint
from flask import render_template, flash, abort


################
#### routes ####
################

@users_blueprint.route('/about')
def about():
    flash('Thanks for learning about this site!', 'info')
    return render_template('users/about.html', company_name='TestDriven.io')


@users_blueprint.route('/admin')
def admin():
    abort(403)
