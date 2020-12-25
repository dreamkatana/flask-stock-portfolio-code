"""
This file (test_watchlist.py) contains the functional tests for the `watchlist` blueprint.
"""


def test_get_add_watch_stock_page(test_client, log_in_default_user):
    """
    GIVEN a Flask application configured for testing and the user logged in
    WHEN the '/watchlist/add_watch_stock' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/watchlist/add_watch_stock')
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Add Stock to Watchlist' in response.data
    assert b'Stock Symbol' in response.data
    assert b'Add' in response.data
