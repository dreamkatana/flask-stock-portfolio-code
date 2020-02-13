from flask import Flask, escape, render_template, request, session, redirect, url_for, flash
from logging.handlers import RotatingFileHandler
import logging

# Create the Flask application
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg', silent=False)
app.config.from_pyfile('flask_sensitive.cfg', silent=True)

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
