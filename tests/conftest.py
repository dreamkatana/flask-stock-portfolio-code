from project import create_app
import pytest
from flask import current_app
from project.models import Stock, User
from project import database
from datetime import datetime

@pytest.fixture(scope='function')
def new_stock():
<<<<<<< HEAD
    stock = Stock('AAPL', 16, 406.78, datetime(2020, 3, 12), 0)
=======
    stock = Stock('AAPL', '16', '406.78')
>>>>>>> part4_user_management
    return stock


@pytest.fixture(scope='module')
def new_user():
    user = User('patrick@email.com', 'FlaskIsAwesome123')
    return user


@pytest.fixture(scope='module')
def register_default_user(init_database):
    user = User('patrick@gmail.com', 'FlaskIsAwesome123')
    database.session.add(user)
    database.session.commit()
    return user


@pytest.fixture(scope='function')
def log_in_default_user(test_client, register_default_user):
    # Log in the user
    test_client.post('/users/login',
                     data={'email': 'patrick@gmail.com',
                           'password': 'FlaskIsAwesome123'},
                     follow_redirects=True)

    yield register_default_user  # this is where the testing happens!

    # Log out the user
    test_client.get('/users/logout', follow_redirects=True)


@pytest.fixture(scope='function')
def confirm_email_default_user(test_client, log_in_default_user):
    # Mark the user as having their email address confirmed
    user = User.query.filter_by(email='patrick@gmail.com').first()
    user.email_confirmed = True
    user.email_confirmed_on = datetime(2020, 7, 8)
    database.session.add(user)
    database.session.commit()

    yield user  # this is where the testing happens!

    # Mark the user as not having their email address confirmed (clean up)
    user = User.query.filter_by(email='patrick@gmail.com').first()
    user.email_confirmed = False
    user.email_confirmed_on = None
    database.session.add(user)
    database.session.commit()


@pytest.fixture(scope='session')
def test_client():
    flask_app = create_app()
    flask_app.config.from_object('config.TestingConfig')
    flask_app.extensions['mail'].suppress = True

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context before accessing the logger
        with flask_app.app_context():
            current_app.logger.info('In the test_client() fixture...')

        yield testing_client  # this is where the testing happens!


@pytest.fixture(scope='module')
def init_database():
    # Create the database and the database table(s)
    database.create_all()

    yield database  # this is where the testing happens!

    database.drop_all()


@pytest.fixture(scope='function')
def afterwards_reset_default_user_password():
    yield  # this is where the testing happens!

    # Since a test using this fixture could change the password for the default user,
    # reset the password back to the default password
    user = User.query.filter_by(email='patrick@gmail.com').first()
    user.set_password('FlaskIsAwesome123')
    database.session.add(user)
    database.session.commit()
