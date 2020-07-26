"""
This file (test_models.py) contains the unit tests for the models.py file.
"""
from datetime import datetime


def test_new_stock(new_stock):
    """
    GIVEN a Stock model
    WHEN a new Stock object is created
    THEN check the symbol, number of shares, purchase price, user ID, and purchase date fields are defined correctly
    """
    assert new_stock.stock_symbol == 'AAPL'
    assert new_stock.number_of_shares == 16
    assert new_stock.purchase_price == 40678
    assert new_stock.user_id == 17
    assert new_stock.purchase_date.year == 2020
    assert new_stock.purchase_date.month == 7
    assert new_stock.purchase_date.day == 18


def test_new_user(test_client_with_app_context, new_user):
    """
    GIVEN a User model
    WHEN a new User object is created
    THEN check the email is valid and hashed password does not equal the password provided
    """
    assert new_user.email == 'patrick@email.com'
    assert new_user.password_hashed != 'FlaskIsAwesome123'


def test_set_password(test_client_with_app_context, new_user):
    """
    GIVEN a User model
    WHEN a new User object is created
    THEN check the password can be changed
    """
    new_user.set_password('FlaskIsStillAwesome456')
    assert new_user.email == 'patrick@email.com'
    assert new_user.password_hashed != 'FlaskIsStillAwesome456'


def test_get_stock_data_success(test_client_with_app_context, mock_requests_get_success_daily, new_stock):
    """
    GIVEN a Flask application and a monkeypatched version of requests.get()
    WHEN the HTTP response is set to successful
    THEN check the HTTP response
    """
    new_stock.get_stock_data()
    assert new_stock.stock_symbol == 'AAPL'
    assert new_stock.number_of_shares == 16
    assert new_stock.purchase_price == 40678
    assert new_stock.purchase_date.year == 2020
    assert new_stock.purchase_date.month == 7
    assert new_stock.purchase_date.day == 18
    assert new_stock.current_price == 14834
    assert new_stock.current_price_date.date() == datetime.now().date()


def test_get_stock_data_failure(test_client_with_app_context, mock_requests_get_failure, new_stock):
    """
    GIVEN a Flask application and a monkeypatched version of requests.get()
    WHEN the HTTP response is set to failed
    THEN check the HTTP response
    """
    new_stock.get_stock_data()
    assert new_stock.stock_symbol == 'AAPL'
    assert new_stock.number_of_shares == 16
    assert new_stock.purchase_price == 40678
    assert new_stock.purchase_date.year == 2020
    assert new_stock.purchase_date.month == 7
    assert new_stock.purchase_date.day == 18
    assert new_stock.current_price == 0
    assert new_stock.current_price_date is None


def test_get_stock_data_success_two_calls(test_client_with_app_context, mock_requests_get_success_daily, new_stock):
    """
    GIVEN a Flask application and a monkeypatched version of requests.get()
    WHEN the HTTP response is set to successful
    THEN check the HTTP response
    """
    assert new_stock.stock_symbol == 'AAPL'
    assert new_stock.current_price == 0
    assert new_stock.current_price_date is None
    new_stock.get_stock_data()
    assert new_stock.current_price == 14834
    assert new_stock.current_price_date.date() == datetime.now().date()
    new_stock.get_stock_data()
    assert new_stock.current_price == 14834
    assert new_stock.current_price_date.date() == datetime.now().date()
