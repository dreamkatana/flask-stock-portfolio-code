from flask import Flask, escape, render_template, request, session, redirect, url_for, flash
from logging.handlers import RotatingFileHandler
import logging
from flask.logging import default_handler

app = Flask(__name__)

# TEMPORARY - Set the secret key to a temporary value!
app.secret_key = 'BAD_SECRET_KEY'

# Logging Configuration
file_handler = RotatingFileHandler('flask-stock-portfolio.log',
                                   maxBytes=16384,
                                   backupCount=20)
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]')
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

# Remove the default logger configured by Flask
app.logger.removeHandler(default_handler)

app.logger.info('Starting the Flask Stock Portfolio App...')


@app.route('/')
def index():
    app.logger.info('Calling the index() function.')
    return render_template('index.html')


@app.route('/about')
def about():
    flash('Thanks for learning about this site!', 'info')
    return render_template('about.html', company_name='TestDriven.io')
    # return render_template('about.html')


@app.route('/stocks/')
def projects():
    return 'The stocks page'


@app.route('/hello/<path:message>')
def hello_message(message):
    return f'<h1>Welcome {escape(message)}!</h1>'


@app.route('/blog_posts/<int:post_id>')
def display_blog_post(post_id):
    return f'<h1>Blog Post #{post_id}...</h1>'


@app.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        # Print the form data to the console
        for key, value in request.form.items():
            print(f'{key}: {value}')

        # Save the form data to the session object
        session['stock_symbol'] = request.form['stock_symbol']
        session['number_of_shares'] = request.form['number_of_shares']
        session['purchase_price'] = request.form['purchase_price']
        flash(f"Added new stock ({ request.form['stock_symbol'] })!", 'success')
        app.logger.info(f"Added new stock ({ request.form['stock_symbol'] })!")
        return redirect(url_for('list_stocks'))

    return render_template('add_stock.html')


@app.route('/list_stocks')
def list_stocks():
    return render_template('stocks.html')
