"""
This file (test_stocks_routes.py) contains the unit tests for testing the
routes (routes.py) in the Stocks blueprint.
"""


def test_index_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Welcome to the Flask Stock Portfolio App!' in response.data


def test_about_page(test_client):
    response = test_client.get('/about')
    assert b'Flask Stock Portfolio App' in response.data
    assert b'About' in response.data
    assert b'This application is built using the Flask web framework.' in response.data
    assert b'Course developed by TestDriven.io.' in response.data


def test_get_add_stock_page(test_client):
    response = test_client.get('/add_stock')
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Add a Stock:' in response.data
    assert b'Stock Symbol:' in response.data
    assert b'Number of Shares:' in response.data
    assert b'Share Price:' in response.data


def test_post_add_stock_page(test_client):
    response = test_client.post('/add_stock',
                                data=dict(stockSymbol='AAPL',
                                          numberOfShares='23',
                                          sharePrice='432.17'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'List of Stocks:' in response.data
    assert b'Stock Symbol' in response.data
    assert b'Number of Shares' in response.data
    assert b'Share Price' in response.data
    assert b'AAPL' in response.data
    assert b'23' in response.data
    assert b'432.17' in response.data
    assert b'Added new stock (AAPL)!' in response.data
