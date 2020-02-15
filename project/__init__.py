from project.stocks import stocks_blueprint
from project.users import users_blueprint
from flask import Flask
from logging.handlers import RotatingFileHandler
import logging


######################################
#### Application Factory Function ####
######################################

def create_app(config_filename='flask.cfg'):
    # Create the Flask application
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename, silent=False)
    app.config.from_pyfile('flask_sensitive.cfg', silent=True)

    register_blueprints(app)
    configure_logging(app)
    return app


def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    app.register_blueprint(stocks_blueprint)
    app.register_blueprint(users_blueprint)


def configure_logging(app):
    # Logging Configuration
    file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]')
    file_handler = RotatingFileHandler('instance/logs/flask-stock-portfolio.log',
                                       maxBytes=16384,
                                       backupCount=20)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('Starting the Flask Stock Portfolio App...')
