"""
The stocks blueprint handles the user management for this application.
Specifically, this blueprint allows for users to add, edit, and delete
stock data from their portfolio.
"""
from flask import Blueprint, current_app

stocks_blueprint = Blueprint('stocks', __name__, template_folder='templates')

from . import routes


###########################
#### request callbacks ####
###########################

@stocks_blueprint.before_request
def stocks_before_request():
    current_app.logger.info('Calling before_request() for the stocks blueprint...')


@stocks_blueprint.after_request
def stocks_after_request(response):
    current_app.logger.info('Calling after_request() for the stocks blueprint...')
    return response


@stocks_blueprint.teardown_request
def stocks_teardown_request(error=None):
    current_app.logger.info('Calling teardown_request() for the stocks blueprint...')