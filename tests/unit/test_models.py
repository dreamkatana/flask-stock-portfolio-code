"""
This file (test_models.py) contains the unit tests for the models.py file.
"""


def test_new_stock(new_stock):
    """
    GIVEN a Stock model
    WHEN a new Stock is created
    THEN check the symbol, number of shares, and share price fields are defined correctly
    """
    assert new_stock.symbol == 'AAPL'
    assert new_stock.shares == 16
    assert new_stock.price == 406.78


def test_new_user(new_user):
    """
    Test that a new user with valid data is created successfully
    """
    assert new_user.email == 'patrick@email.com'
    assert new_user.password_hashed != 'FlaskIsAwesome123'


