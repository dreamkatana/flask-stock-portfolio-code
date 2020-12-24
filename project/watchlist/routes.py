from . import watchlist_blueprint
from flask import render_template


@watchlist_blueprint.route('/watchlist')
def watchlist():
    return render_template('watchlist/watchlist.html')
