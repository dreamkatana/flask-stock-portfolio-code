from flask import Flask, escape, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from logging.handlers import RotatingFileHandler
import logging
import os


# Determine the folder of the top-level directory of this project
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Create the Flask application
app = Flask(__name__)

# Database Configuration (SQLAlchemy)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASEDIR, 'instance', 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure the Flask extensions
database = SQLAlchemy(app)
db_migration = Migrate(app, database)

import models
from models import Stock

# Logging Configuration
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]')
file_handler = RotatingFileHandler('instance/logs/flask-stock-portfolio.log',
                                   maxBytes=16384,
                                   backupCount=20)
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.info('Starting the Flask Stock Portfolio App...')

# TEMPORARY - Set the secret key to a temporary value!
app.secret_key = 'BAD_SECRET_KEY'


@app.route('/')
def index():
    app.logger.info('Calling the index() function.')
    return render_template('index.html')


@app.route('/about')
def about():
    flash('Thanks for learning about this site!', 'info')
    return render_template('about.html', company_name='TestDriven.io')


@app.route('/users/<username>')
def user_profile(username):
    return f'<h1>Welcome {escape(username)}!</h1>'


@app.route('/blog_posts/<int:post_id>')
def display_blog_post(post_id):
    return f'<h1>Blog Post #{post_id}...</h1>'


@app.route('/add_stock', methods=['GET', 'POST'])
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
        app.logger.info(f"Added new stock ({ request.form['stockSymbol'] })!")
        return redirect(url_for('list_stocks'))
    else:
        return render_template('add_stock.html')


@app.route('/stocks')
def list_stocks():
    stocks = Stock.query.order_by(Stock.id).all()
    return render_template('stocks.html', stocks=stocks)
