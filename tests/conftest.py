import pytest
from project import create_app, database
from project.models import Stock, User


@pytest.fixture(scope='module')
def new_stock():
    stock = Stock('AAPL', 16, 406.78)
    return stock


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('flask_test.cfg')

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    # Create the database and the database table
    database.create_all()

    yield database  # this is where the testing happens!

    database.drop_all()


@pytest.fixture(scope='module')
def new_user():
    user = User('patrick@email.com', 'FlaskIsAwesome123')
    return user
