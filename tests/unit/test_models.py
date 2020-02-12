"""
This file (test_models.py) contains the unit tests for the models.py file.
"""


def test_new_stock(new_stock):
    """
    GIVEN a Stock model
    WHEN a new Stock is created
    THEN check the symbol, number of shares, and share price fields are defined correctly
    """
    assert stock.symbol == 'AAPL'
    assert stock.shares == 16
    assert stock.price == 406.78
