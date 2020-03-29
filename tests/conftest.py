import pytest
from project import create_app, database
from project.models import Stock, User
from datetime import datetime
import requests


########################
#### Helper Classes ####
########################

class MockSuccessResponseDaily(object):
    def __init__(self, url):
        self.status_code = 200
        self.url = url

    def json(self):
        return {
            'Meta Data': {
                "2. Symbol": "AAPL",
                "3. Last Refreshed": "2020-03-24"
            },
            'Time Series (Daily)': {
                "2020-03-24": {
                    "4. close": "148.3400",
                },
                "2020-03-23": {
                    "4. close": "135.9800",
                }
            }
        }


class MockSuccessResponseWeekly(object):
    def __init__(self, url):
        self.status_code = 200
        self.url = url

    def json(self):
        return {
            'Meta Data': {
                "2. Symbol": "AAPL",
                "3. Last Refreshed": "2020-03-27"
            },
            'Weekly Adjusted Time Series': {
                "2020-03-27": {
                    "4. close": "148.3400",
                },
                "2020-03-20": {
                    "4. close": "135.9800",
                }
            }
        }


class MockFailedResponse(object):
    def __init__(self, url):
        self.status_code = 404
        self.url = url

    def json(self):
        return {'error': 'bad'}


##################
#### Fixtures ####
##################

@pytest.fixture(scope='function')
def new_stock():
    stock = Stock('AAPL', 16, 406.78, datetime(2020, 3, 12), 0)
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


@pytest.fixture(scope='module')
def register_default_user(init_database):
    user = User('patrick@gmail.com', 'FlaskIsAwesome123')
    database.session.add(user)
    database.session.commit()
    return user


@pytest.fixture(scope='function')
def log_in_user(test_client, register_default_user):
    # Log in the user
    response = test_client.post('/login',
                     data=dict(email='patrick@gmail.com', password='FlaskIsAwesome123'),
                     follow_redirects=True)
    print(f'Login Response: \n{response.data}')

    yield register_default_user  # this is where the testing happens!

    # Since some unit tests are changing the password for the default user,
    # reset the password back to the default password
    response = test_client.post('/password_change',
                                data=dict(password='FlaskIsAwesome123'),
                                follow_redirects=True)
    print(f'Password Change (to default): \n{response.data}')

    # Log out the user
    test_client.get('/logout', follow_redirects=True)


@pytest.fixture(scope='function')
def confirm_email_user(test_client, log_in_user):
    # Log in the user
    test_client.post('/login',
                     data=dict(email='patrick@gmail.com', password='FlaskIsAwesome123'),
                     follow_redirects=True)

    user = User.query.filter_by(email='patrick@gmail.com').first()
    user.email_confirmed = True
    user.email_confirmed_on = datetime(2020, 3, 10)
    database.session.add(user)
    database.session.commit()

    yield user  # this is where the testing happens!

    user.email_confirmed = False
    user.email_confirmed_on = None
    database.session.add(user)
    database.session.commit()


@pytest.fixture(scope='module')
def stocks_blueprint_user_registration(test_client, init_database):
    # Create two users
    user1 = User('patrick1@gmail.com', 'FlaskIsAwesome123')
    user2 = User('patrick2@gmail.com', 'FlaskIsReallyAwesome123')
    database.session.add(user1)
    database.session.add(user2)
    database.session.commit()


@pytest.fixture(scope='function')
def stocks_blueprint_login_user1(test_client, stocks_blueprint_user_registration):
    # Login User 1
    response = test_client.post('/login', data=dict(email='patrick1@gmail.com', password='FlaskIsAwesome123'))
    print(f'Login response: {response.data}')

    yield  # this is where the testing happens!

    # Logout User 1
    test_client.get('/logout', follow_redirects=True)


@pytest.fixture(scope='function')
def stocks_blueprint_login_user2(test_client, stocks_blueprint_user_registration):
    # Login User 2
    response = test_client.post('/login', data=dict(email='patrick2@gmail.com', password='FlaskIsReallyAwesome123'))
    print(f'Login response: {response.data}')

    yield  # this is where the testing happens!

    # Logout User 2
    test_client.get('/logout', follow_redirects=True)


@pytest.fixture(scope='function')
def stocks_blueprint_user_login(test_client, stocks_blueprint_user_registration, stocks_blueprint_login_user1):
    # Login User 1
    response = test_client.post('/login', data=dict(email='patrick1@gmail.com', password='FlaskIsAwesome123'))
    print(f'Login response: {response.data}')

    # Create three new stock entries for User 1
    test_client.post('/add_stock', data=dict(symbol='AAPL',
                                             shares='23',
                                             price='432.17',
                                             purchase_date_month='4',
                                             purchase_date_day='23',
                                             purchase_date_year='2019'))
    test_client.post('/add_stock', data=dict(symbol='COST',
                                             shares='27',
                                             price='295.67',
                                             purchase_date_month='5',
                                             purchase_date_day='30',
                                             purchase_date_year='2018'))
    response = test_client.post('/add_stock', data=dict(symbol='HD',
                                                        shares='35',
                                                        price='190.56',
                                                        purchase_date_month='12',
                                                        purchase_date_day='11',
                                                        purchase_date_year='2017'))
    print(f'Add Stock (HD) response: {response.data}')

    yield  # this is where the testing happens!

    # Logout User 1
    test_client.get('/logout', follow_redirects=True)


@pytest.fixture(scope='function')
def mock_requests_get_success_daily(monkeypatch):
    # Create a mock for the requests.get() call to prevent making the actual API call
    def mock_get(url):
        return MockSuccessResponseDaily(url)

    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=MSFT&apikey=demo'
    monkeypatch.setattr(requests, 'get', mock_get)


@pytest.fixture(scope='function')
def mock_requests_get_failure(monkeypatch):
    def mock_get(url):
        return MockFailedResponse(url)

    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=MSFT&apikey=demo'
    monkeypatch.setattr(requests, 'get', mock_get)


@pytest.fixture(scope='function')
def mock_requests_get_success_weekly(monkeypatch):
    # Create a mock for the requests.get() call to prevent making the actual API call
    def mock_get(url):
        return MockSuccessResponseWeekly(url)

    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=MSFT&apikey=demo'
    monkeypatch.setattr(requests, 'get', mock_get)
