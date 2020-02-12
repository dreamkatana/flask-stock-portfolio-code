from flask import Flask, escape, render_template, request, session, redirect, url_for, flash
from logging.handlers import RotatingFileHandler
import logging

app = Flask(__name__)

# blueprints
from project.stocks import stocks_blueprint
from project.users import users_blueprint

# register the blueprints
app.register_blueprint(stocks_blueprint)
app.register_blueprint(users_blueprint)

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


# @app.route('/')
# def index():
#     app.logger.info('Calling the index() function.')
#     return render_template('index.html')
#
#
# @app.route('/about')
# def about():
#     flash('Thanks for learning about this site!', 'info')
#     return render_template('about.html', company_name='TestDriven.io')
#
#
# @app.route('/users/<username>')
# def user_profile(username):
#     return f'<h1>Welcome {escape(username)}!</h1>'
#
#
# @app.route('/blog_posts/<int:post_id>')
# def display_blog_post(post_id):
#     return f'<h1>Blog Post #{post_id}...</h1>'
#
#
# @app.route('/add_stock', methods=['GET', 'POST'])
# def add_stock():
#     if request.method == 'POST':
#         # DEBUG - Print the form data to the console
#         for key, value in request.form.items():
#             print(f'{key}: {value}')
#
#         # Save the form data to the session object
#         session['stockSymbol'] = request.form['stockSymbol']
#         session['numberOfShares'] = request.form['numberOfShares']
#         session['sharePrice'] = request.form['sharePrice']
#         flash(f"Added new stock ({ request.form['stockSymbol'] })!", 'success')
#         app.logger.info(f"Added new stock ({ request.form['stockSymbol'] })!")
#         return redirect(url_for('list_stocks'))
#     else:
#         return render_template('add_stock.html')
#
#
# @app.route('/stocks')
# def list_stocks():
#     return render_template('stocks.html')
