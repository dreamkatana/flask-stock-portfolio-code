from . import watchlist_blueprint
from flask import render_template
from flask_login import login_required
from .forms import WatchStockForm


@watchlist_blueprint.route('/watchlist')
@login_required
def watchlist():
    return render_template('watchlist/watchlist.html')


@watchlist_blueprint.route('/watchlist/add_watch_stock')
@login_required
def add_watch_stock():
    form = WatchStockForm()
    return render_template('watchlist/add_watch_stock.html', form=form)
