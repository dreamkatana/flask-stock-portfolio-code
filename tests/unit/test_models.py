"""
This file (test_models.py) contains the unit tests for the models.py file.
"""
from datetime import datetime


def test_new_stock(new_stock):
    """
    GIVEN a Stock model
    WHEN a new Stock is created
    THEN check the symbol, number of shares, and share price fields are defined correctly
    """
    assert new_stock.symbol == 'AAPL'
    assert new_stock.shares == 16
    assert new_stock.purchase_price == 406.78
    assert new_stock.purchase_date.date() == datetime(2020, 3, 12).date()


def test_new_user(new_user):
    """
    Test that a new user with valid data is created successfully
    """
    assert new_user.email == 'patrick@email.com'
    assert new_user.password_hashed != 'FlaskIsAwesome123'


def test_set_password(new_user):
    """
    Test that the password can be set for the user
    """
    new_user.set_password('FlaskIsStillAwesome456')
    assert new_user.email == 'patrick@email.com'
    assert new_user.password_hashed != 'FlaskIsStillAwesome456'


def test_get_stock_data_success(test_client, mock_requests_get_success, new_stock):
    """
    GIVEN a Flask application and a monkeypatched version of requests.get()
    WHEN the HTTP response is set to successful
    THEN check the HTTP response
    """
    new_stock.get_stock_data()
    assert new_stock.symbol == 'AAPL'
    assert new_stock.shares == 16
    assert new_stock.purchase_price == 406.78
    assert new_stock.purchase_date.date() == datetime(2020, 3, 12).date()
    assert new_stock.current_price == 148.34
    assert new_stock.current_price_date.date() == datetime(2020, 3, 24).date()
    assert new_stock.position_value == (148.34*16)


def test_get_stock_data_failure(test_client, mock_requests_get_failure, new_stock):
    """
    GIVEN a Flask application and a monkeypatched version of requests.get()
    WHEN the HTTP response is set to failed
    THEN check the HTTP response
    """
    new_stock.get_stock_data()
    assert new_stock.symbol == 'AAPL'
    assert new_stock.shares == 16
    assert new_stock.purchase_price == 406.78
    assert new_stock.purchase_date.date() == datetime(2020, 3, 12).date()
    assert new_stock.current_price == 0.0
    assert new_stock.current_price_date is None
    assert new_stock.position_value == 0.0


def test_get_stock_data_success_two_calls(test_client, mock_requests_get_success, new_stock):
    """
    GIVEN a Flask application and a monkeypatched version of requests.get()
    WHEN the HTTP response is set to successful
    THEN check the HTTP response
    """
    assert new_stock.symbol == 'AAPL'
    assert new_stock.current_price == 0.0
    assert new_stock.current_price_date is None
    assert new_stock.position_value == 0.0
    new_stock.get_stock_data()
    assert new_stock.symbol == 'AAPL'
    assert new_stock.current_price == 148.34
    assert new_stock.current_price_date.date() == datetime(2020, 3, 24).date()
    assert new_stock.position_value == (148.34*16)
    new_stock.get_stock_data()
    assert new_stock.symbol == 'AAPL'
    assert new_stock.current_price == 148.34
    assert new_stock.current_price_date.date() == datetime(2020, 3, 24).date()
    assert new_stock.position_value == (148.34*16)
