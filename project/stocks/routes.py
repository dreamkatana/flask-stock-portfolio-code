#################
#### imports ####
#################
from . import stocks_blueprint
from flask import render_template, request, redirect, url_for, flash, current_app
from project.models import Stock
from project import database
import click


###########################
#### request callbacks ####
###########################

# @stocks_blueprint.before_request
# def stocks_before_request():
#     current_app.logger.info('Calling before_request() for the stocks blueprint...')
#
#
# @stocks_blueprint.after_request
# def stocks_after_request(response):
#     current_app.logger.info('Calling after_request() for the stocks blueprint...')
#     return response
#
#
# @stocks_blueprint.teardown_request
# def stocks_teardown_request(error=None):
#     current_app.logger.info('Calling teardown_request() for the stocks blueprint...')


######################
#### cli commands ####
######################

@stocks_blueprint.cli.command('create_default_set')
def create_default_set():
    """Create three new stocks and add them to the database"""
    stock1 = Stock('HD', '25', '247.29')
    stock2 = Stock('TWTR', '230', '31.89')
    stock3 = Stock('DIS', '65', '118.77')
    database.session.add(stock1)
    database.session.add(stock2)
    database.session.add(stock3)
    database.session.commit()


@stocks_blueprint.cli.command('create')
@click.argument('symbol')
@click.argument('number_of_shares')
@click.argument('purchase_price')
def create(symbol, number_of_shares, purchase_price):
    """Create a new stock and add it to the database"""
    stock = Stock(symbol, number_of_shares, purchase_price)
    database.session.add(stock)
    database.session.commit()


################
#### routes ####
################

@stocks_blueprint.route('/')
def index():
    current_app.logger.info('Calling the index() function.')
    return render_template('stocks/index.html')


@stocks_blueprint.route('/add_stock', methods=['GET', 'POST'])
@login_required
def add_stock():
    if request.method == 'POST':
        # Save the form data to the database
        new_stock = Stock(request.form['stock_symbol'],
                          request.form['number_of_shares'],
                          request.form['purchase_price'])
        database.session.add(new_stock)
        database.session.commit()

        flash(f"Added new stock ({ request.form['stock_symbol'] })!", 'success')
        current_app.logger.info(f"Added new stock ({ request.form['stock_symbol'] })!")
        return redirect(url_for('stocks.list_stocks'))
    else:
        return render_template('stocks/add_stock.html')


@stocks_blueprint.route('/stocks')
@login_required
def list_stocks():
    stocks = Stock.query.order_by(Stock.id).filter_by(user_id=current_user.id).all()

    current_account_value = 0.0
    for stock in stocks:
        return_value = stock.get_stock_data()
        if return_value != '':
            flash(return_value, 'error')
            break
        current_account_value += stock.position_value

    database.session.commit()
    return render_template('stocks/stocks.html', stocks=stocks, value=round(current_account_value, 2))


@stocks_blueprint.route('/delete_stock/<id>', methods=['GET', 'POST'])
@login_required
def delete_stock(id):
    stock = Stock.query.filter_by(id=id).first()

    if stock.user_id == current_user.id:
        form = DeleteStock()

        if form.validate_on_submit():
            database.session.delete(stock)
            database.session.commit()
            flash(f'Stock ({stock.symbol}) was deleted!', 'info')
            return redirect(url_for('stocks.list_stocks'))

        return render_template('stocks/delete_stock.html', form=form, stock=stock)
    else:
        return render_template('403.html'), 403


@stocks_blueprint.route('/edit_stock/<id>', methods=['GET', 'POST'])
@login_required
def edit_stock(id):
    stock = Stock.query.filter_by(id=id).first()

    if stock.user_id == current_user.id:
        form = EditStock()

        if form.validate_on_submit():
            stock.update_data(form.shares.data,
                              form.price.data,
                              datetime(form.purchase_date_year.data,
                                       form.purchase_date_month.data,
                                       form.purchase_date_day.data))
            database.session.add(stock)
            database.session.commit()
            flash(f'Stock ({stock.symbol}) has been updated!', 'info')
            return redirect(url_for('stocks.list_stocks'))

        return render_template('stocks/edit_stock.html', form=form, stock=stock)
    else:
        return render_template('403.html'), 403


@stocks_blueprint.route("/chartjs_demo1")
def chartjs_demo1():
    return render_template('stocks/chartjs_demo1.html')


@stocks_blueprint.route("/chartjs_demo2")
def chartjs_demo2():
    title = 'Monthly Data'
    labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August']
    values = [10.3, 9.2, 8.7, 7.1, 6.0, 4.4, 7.6, 8.9]
    return render_template('stocks/chartjs_demo2.html', values=values, labels=labels, title=title)


@stocks_blueprint.route("/chartjs_demo3")
def chartjs_demo3():
    title = 'Daily Prices'
    labels = [datetime(2020, 2, 10),   # Monday 2/10/2020
              datetime(2020, 2, 11),   # Tuesday 2/11/2020
              datetime(2020, 2, 12),   # Wednesday 2/12/2020
              datetime(2020, 2, 13),   # Thursday 2/13/2020
              datetime(2020, 2, 14),   # Friday 2/14/2020
              datetime(2020, 2, 17),   # Monday 2/17/2020
              datetime(2020, 2, 18),   # Tuesday 2/18/2020
              datetime(2020, 2, 19)]   # Wednesday 2/19/2020
    values = [10.3, 9.2, 8.7, 7.1, 6.0, 4.4, 7.6, 8.9]
    return render_template('stocks/chartjs_demo3.html', values=values, labels=labels, title=title)


@stocks_blueprint.route('/stock/<id>')
@login_required
def stock_details(id):
    stock = Stock.query.filter_by(id=id).first()

    if stock.user_id == current_user.id:
        title = ''
        labels = []
        values = []

        url = create_alpha_vantage_get_url_weekly(stock.symbol)

        try:
            r = requests.get(url)

            if r.status_code == 200:
                weekly_data = r.json()
                title = f'Weekly Prices ({stock.symbol})'

                for element in weekly_data['Weekly Adjusted Time Series']:
                    date = datetime.fromisoformat(element).date()
                    if date > stock.purchase_date.date():
                        labels.append(date)
                        values.append(weekly_data['Weekly Adjusted Time Series'][element]['4. close'])

                labels.reverse()
                values.reverse()
        except requests.exceptions.ConnectionError:
            flash('Error! Network problem preventing retrieving the stock data!', 'error')

        return render_template('stocks/stock_details.html', stock=stock, labels=labels, values=values, title=title)
    else:
        return render_template('403.html'), 403
