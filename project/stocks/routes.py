#################
#### imports ####
#################
from . import stocks_blueprint
from flask import escape, render_template, request, session, redirect, url_for, flash, current_app
from project.models import Stock
from project import database
from .forms import AddStockForm

################
#### routes ####
################

@stocks_blueprint.route('/')
def index():
    current_app.logger.info('Calling the index() function.')
    return render_template('stocks/index.html')


@stocks_blueprint.route('/about')
def about():
    flash('Thanks for learning about this site!', 'info')
    return render_template('stocks/about.html', company_name='TestDriven.io')


@stocks_blueprint.route('/blog_posts/<int:post_id>')
def display_blog_post(post_id):
    return f'<h1>Blog Post #{post_id}...</h1>'


@stocks_blueprint.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    form = AddStockForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            new_stock = Stock(form.symbol.data,
                              form.shares.data,
                              form.price.data)
            database.session.add(new_stock)
            database.session.commit()
            database.session.commit()

            flash(f"Added new stock ({ form.symbol.data })!", 'success')
            current_app.logger.info(f"Added new stock ({ form.symbol.data })!")
            return redirect(url_for('stocks.list_stocks'))
        else:
            flash(f"Error in form data!")

    return render_template('stocks/add_stock.html', form=form)


@stocks_blueprint.route('/stocks')
def list_stocks():
    stocks = Stock.query.order_by(Stock.id).all()
    return render_template('stocks/stocks.html', stocks=stocks)
