from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from logging.handlers import RotatingFileHandler
import logging


#######################
#### Configuration ####
#######################

# Create the instances of the Flask extensions (flask-sqlalchemy, etc.) in
# the global scope, but without any arguments passed in.  These instances are
# not attached to the Flask application at this point.
database = SQLAlchemy()
db_migration = Migrate()


######################################
#### Application Factory Function ####
######################################

def create_app(config_filename=None, include_override_config=False):
    # Create the Flask application
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename, silent=False)
    if include_override_config:
        app.config.from_pyfile('flask_override.cfg', silent=True)
    initialize_extensions(app)
    register_blueprints(app)
    configure_logging(app)
    return app


##########################
#### Helper Functions ####
##########################

def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    database = SQLAlchemy(app)
    db_migration = Migrate(app, database)


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
    app.logger.info(f"  SQLite Database location: {app.config['SQLALCHEMY_DATABASE_URI']}")
    app.logger.info(f"  Secret Key: {app.config['SECRET_KEY']}")


def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from project.stocks import stocks_blueprint
    from project.users import users_blueprint

    app.register_blueprint(stocks_blueprint)
    app.register_blueprint(users_blueprint)
