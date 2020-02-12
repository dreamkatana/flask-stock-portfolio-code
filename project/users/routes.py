#################
#### imports ####
#################
from . import users_blueprint


################
#### routes ####
################

@users_blueprint.route('/users/<username>')
def user_profile(username):
    return f'<h1>Welcome {escape(username)}!</h1>'
