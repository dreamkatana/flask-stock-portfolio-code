#################
#### imports ####
#################
from . import stocks_blueprint
from flask import escape, render_template, request, session, redirect, url_for, flash, current_app
from project.models import Stock
from project import database


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
    if request.method == 'POST':
        # DEBUG - Print the form data to the console
        for key, value in request.form.items():
            print(f'{key}: {value}')

        new_stock = Stock(request.form['stockSymbol'],
                          request.form['numberOfShares'],
                          request.form['sharePrice'])
        database.session.add(new_stock)
        database.session.commit()

        flash(f"Added new stock ({ request.form['stockSymbol'] })!", 'success')
        current_app.logger.info(f"Added new stock ({ request.form['stockSymbol'] })!")
        return redirect(url_for('stocks.list_stocks'))
    else:
        return render_template('stocks/add_stock.html')


@stocks_blueprint.route('/stocks')
def list_stocks():
    stocks = Stock.query.order_by(Stock.id).all()
    return render_template('stocks/stocks.html', stocks=stocks)
