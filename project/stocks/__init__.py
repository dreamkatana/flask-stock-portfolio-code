"""
The stocks Blueprint handles the processing of stock data for this application.
Specifically, this Blueprint allows for users to add, edit, and delete stocks
from their portfolios.
"""
from flask import Blueprint

stocks_blueprint = Blueprint('stocks', __name__, template_folder='templates')

from . import routes
