import pytest
from project import create_app


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('flask_test.cfg')

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    yield testing_client  # this is where the testing happens!
