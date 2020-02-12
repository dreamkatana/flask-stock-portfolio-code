import pytest


@pytest.fixture(scope='module')
def new_stock():
    stock = Stock('AAPL', 16, 406.78)
    return stock
