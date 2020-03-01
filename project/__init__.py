from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from logging.handlers import RotatingFileHandler
import logging


#######################
#### Configuration ####
#######################

# Create the instances of the Flask extensions (flask-sqlalchemy, flask-migrate,
# etc.) in the global scope, but without any arguments passed in.  These instances
# are not attached to the Flask application at this point.
database = SQLAlchemy()
db_migration = Migrate()
bcrypt = Bcrypt()
login = LoginManager()
login.login_view = "users.login"


######################################
#### Application Factory Function ####
######################################

def create_app(config_filename='flask.cfg'):
    # Create the Flask application
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename, silent=False)
    app.config.from_pyfile('flask_sensitive.cfg', silent=True)

    initialize_extensions(app)
    register_blueprints(app)
    configure_logging(app)
    register_error_pages(app)
    return app


##########################
#### Helper Functions ####
##########################

def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    database.init_app(app)
    db_migration.init_app(app, database)
    bcrypt.init_app(app)
    login.init_app(app)

    # Flask-Login configuration
    from project.models import User

    @login.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()


def register_blueprints(app):
    from project.stocks import stocks_blueprint
    from project.users import users_blueprint

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


def register_error_pages(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(405)
    def page_not_found(e):
        return render_template('405.html'), 405

    @app.errorhandler(403)
    def page_forbidden(e):
        return render_template('403.html'), 403

    @app.errorhandler(410)
    def page_gone(e):
        return render_template('410.html'), 410
