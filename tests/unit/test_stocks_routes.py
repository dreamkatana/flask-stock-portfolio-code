"""
This file (test_stocks_routes.py) contains the unit tests for testing the
routes (routes.py) in the Stocks blueprint.
"""


def test_index_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Welcome to the Flask Stock Portfolio App!' in response.data


def test_home_page_post(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = test_client.post('/')
    assert response.status_code == 405
    assert b'Welcome to the Flask Stock Portfolio App!' not in response.data


def test_about_page(test_client):
    response = test_client.get('/about')
    assert b'Flask Stock Portfolio App' in response.data
    assert b'About' in response.data
    assert b'This application is built using the Flask web framework.' in response.data
    assert b'Course developed by TestDriven.io.' in response.data


def test_get_add_stock_page(test_client, stocks_blueprint_user_login):
    response = test_client.get('/add_stock')
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Add a Stock:' in response.data
    assert b'Stock Symbol:' in response.data
    assert b'Number of Shares:' in response.data
    assert b'Share Price:' in response.data


def test_get_add_stock_page_not_logged_in(test_client):
    response = test_client.get('/add_stock', follow_redirects=True)
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Add a Stock:' not in response.data
    assert b'Please log in to access this page.' in response.data


def test_post_add_stock_page(test_client, mock_requests_get_success_daily, stocks_blueprint_user_login):
    response = test_client.post('/add_stock',
                                data=dict(symbol='AAPL',
                                          shares='23',
                                          price='432.17',
                                          purchase_date_month='4',
                                          purchase_date_day='23',
                                          purchase_date_year='2019'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'List of Stocks:' in response.data
    assert b'Stock Symbol' in response.data
    assert b'Number of Shares' in response.data
    assert b'Share Price' in response.data
    assert b'AAPL' in response.data
    assert b'23' in response.data
    assert b'432.17' in response.data
    assert b'4/23/2019' in response.data
    assert b'Added new stock (AAPL)!' in response.data


def test_post_add_stock_page_not_logged_in(test_client):
    response = test_client.post('/add_stock',
                                data=dict(symbol='AAPL',
                                          shares='23',
                                          price='432.17',
                                          purchase_date_month='4',
                                          purchase_date_day='23',
                                          purchase_date_year='2019'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'List of Stocks:' not in response.data
    assert b'Please log in to access this page.' in response.data


def test_post_add_stock_no_data(test_client, stocks_blueprint_user_login):
    response = test_client.post('/add_stock',
                                data=dict(stockSymbol='',
                                          numberOfShares='',
                                          sharePrice='',
                                          purchase_date_month='',
                                          purchase_date_day='',
                                          purchase_date_year=''),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Error in form data!' in response.data
    assert b'Added new stock ()!' not in response.data
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Add a Stock:' in response.data
    assert b'Stock Symbol:' in response.data
    assert b'Number of Shares:' in response.data
    assert b'Share Price:' in response.data


def test_post_add_stock_only_symbol_data(test_client, stocks_blueprint_user_login):
    response = test_client.post('/add_stock',
                                data=dict(stockSymbol='SAM',
                                          numberOfShares='',
                                          sharePrice='',
                                          purchase_date_month='',
                                          purchase_date_day='',
                                          purchase_date_year=''),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Error in form data!' in response.data
    assert b'Added new stock (SAM)!' not in response.data
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Add a Stock:' in response.data
    assert b'Stock Symbol:' in response.data
    assert b'Number of Shares:' in response.data
    assert b'Share Price:' in response.data


def test_post_add_stock_invalid_number_of_shares(test_client, stocks_blueprint_user_login):
    response = test_client.post('/add_stock',
                                data=dict(stockSymbol='SAM',
                                          numberOfShares='I_AM_INCORRECT_DATA',
                                          sharePrice='123.45',
                                          purchase_date_month='4',
                                          purchase_date_day='23',
                                          purchase_date_year='2019'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Error in form data!' in response.data
    assert b'Added new stock (SAM)!' not in response.data
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Add a Stock:' in response.data
    assert b'Stock Symbol:' in response.data
    assert b'Number of Shares:' in response.data
    assert b'Share Price:' in response.data


def test_get_stock_data_logged_in(test_client, mock_requests_get_success_daily, stocks_blueprint_user_login):
    """
    GIVEN a Flask application with a user logged in
    WHEN the '/stocks' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/stocks', follow_redirects=True)
    print(response.data)
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Stock Symbol' in response.data
    assert b'Number of Shares' in response.data
    assert b'Purchase Price' in response.data
    assert b'Purchase Date' in response.data
    assert b'Current Share Price' in response.data
    assert b'Stock Position Value' in response.data
    assert b'Actions' in response.data
    assert b'AAPL' in response.data
    assert b'COST' in response.data
    assert b'HD' in response.data
    assert b'Delete' in response.data
    assert b'Edit' in response.data
    assert b'TOTAL VALUE' in response.data


def test_get_stock_data_not_logged_in(test_client, init_database):
    """
    GIVEN a Flask application with a user not logged in
    WHEN the '/stocks' page is requested (GET)
    THEN check that no data is displayed and the user is redirected to the Login page
    """
    response = test_client.get('/stocks', follow_redirects=True)
    print(response.data)
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'AAPL' not in response.data
    assert b'COST' not in response.data
    assert b'HD' not in response.data
    assert b'Please log in to access this page.' in response.data


def test_get_delete_stock_valid_owner(test_client, stocks_blueprint_user_login):
    """
    GIVEN a Flask application with a user logged in
    WHEN the '/delete_stock/2' page is requested (GET) from the user that owns that stock
    THEN check the response is valid
    """
    response = test_client.get('/delete_stock/2', follow_redirects=True)
    print(response.data)
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Click below to delete COST (27 shares purchased on 05/30/2018) from your portfolio:' in response.data
    assert b'Delete Stock' in response.data


def test_get_delete_stock_invalid_owner(test_client, stocks_blueprint_user_registration, stocks_blueprint_login_user2):
    """
    GIVEN a Flask application with a user logged in
    WHEN the '/delete_stock/2' page is requested (GET) from a user that does NOT own the stock
    THEN check that a 403 error is returned
    """
    response = test_client.get('/delete_stock/2', follow_redirects=True)
    print(response.data)
    assert response.status_code == 403
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Click below to delete' not in response.data
    assert b'Delete Stock' not in response.data
    assert b"You don't have the permission to access the requested resource." in response.data


def test_post_delete_stock_valid_owner(test_client, stocks_blueprint_user_login, mock_requests_get_success_daily):
    """
    GIVEN a Flask application with a user logged in
    WHEN the '/delete_stock/2' page is posted to (POST) from the user that owns that stock
    THEN check the response is valid
    """
    response = test_client.post('/delete_stock/2', follow_redirects=True)
    print(response.data)
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Stock (COST) was deleted!' in response.data
    assert b'List of Stocks' in response.data


def test_post_delete_stock_invalid_owner(test_client, stocks_blueprint_user_registration, stocks_blueprint_login_user2):
    """
    GIVEN a Flask application with a user logged in
    WHEN the '/delete_stock/1' page is posted to (POST) from a user that does NOT own the stock
    THEN check that a 403 error is returned
    """
    response = test_client.post('/delete_stock/1', follow_redirects=True)
    print(response.data)
    assert response.status_code == 403
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Stock (COST) was deleted!' not in response.data
    assert b'List of Stocks' not in response.data
    assert b"You don't have the permission to access the requested resource." in response.data


def test_get_edit_stock_valid_owner(test_client, stocks_blueprint_user_login):
    """
    GIVEN a Flask application with a user logged in
    WHEN the '/edit_stock/3' page is requested (GET) from the user that owns that stock
    THEN check the response is valid
    """
    response = test_client.get('/edit_stock/1', follow_redirects=True)
    print(response.data)
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Stock: AAPL' in response.data
    assert b'Edit Stock' in response.data


def test_get_edit_stock_invalid_owner(test_client, stocks_blueprint_user_registration, stocks_blueprint_login_user2):
    """
    GIVEN a Flask application with a user logged in
    WHEN the '/edit_stock/3' page is requested (GET) from a user that does NOT own the stock
    THEN check that a 403 error is returned
    """
    response = test_client.get('/edit_stock/3', follow_redirects=True)
    print(response.data)
    assert response.status_code == 403
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Stock: AAPL' not in response.data
    assert b'Edit Stock' not in response.data
    assert b"You don't have the permission to access the requested resource." in response.data


def test_post_edit_stock_valid_owner_valid_data(test_client, stocks_blueprint_user_login, mock_requests_get_success_daily):
    """
    GIVEN a Flask application with a user logged in
    WHEN the '/edit_stock/3' page is posted to (POST) from the user that owns that stock
    THEN check the response is valid
    """
    response = test_client.post('/edit_stock/3',
                                data=dict(shares='25',
                                          price='222.33',
                                          purchase_date_month='5',
                                          purchase_date_day='30',
                                          purchase_date_year='2018'),
                                follow_redirects=True)
    print(response.data)
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Stock (HD) has been updated!' in response.data
    assert b'List of Stocks' in response.data


def test_post_edit_stock_valid_owner_invalid_data(test_client, stocks_blueprint_user_login, mock_requests_get_success_daily):
    """
    GIVEN a Flask application with a user logged in
    WHEN the '/edit_stock/3' page is posted to (POST) from the user that owns that stock
    THEN check the response is valid
    """
    response = test_client.post('/edit_stock/3',
                                data=dict(shares='25',
                                          price='',
                                          purchase_date_month='5',
                                          purchase_date_day='30',
                                          purchase_date_year='2018'),
                                follow_redirects=True)
    print(response.data)
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Stock: HD' in response.data
    assert b'This field is required.' in response.data
    assert b'Stock (AAPL) has been updated!' not in response.data
    assert b'List of Stocks' not in response.data


def test_post_edit_stock_invalid_owner(test_client, stocks_blueprint_user_registration, stocks_blueprint_login_user2):
    """
    GIVEN a Flask application with a user logged in
    WHEN the '/edit_stock/3' page is posted to (POST) from a user that does NOT own the stock
    THEN check the response is valid
    """
    response = test_client.post('/edit_stock/3',
                                data=dict(numberOfShares='25',
                                          sharePrice='222.33',
                                          purchase_date_month='5',
                                          purchase_date_day='30',
                                          purchase_date_year='2018'),
                                follow_redirects=True)
    print(response.data)
    assert response.status_code == 403
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Stock (AAPL) has been updated!' not in response.data
    assert b'List of Stocks' not in response.data
    assert b"You don't have the permission to access the requested resource." in response.data


def test_get_stock_details_valid_owner_valid_response(test_client, stocks_blueprint_user_login, mock_requests_get_success_weekly):
    """
    GIVEN a Flask application with a user logged in
    WHEN the '/stock/1' page is requested (GET) from the user that owns that stock
    THEN check the response is valid
    """
    response = test_client.get('/stock/1', follow_redirects=True)
    print(response.data)
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Symbol: AAPL' in response.data
    assert b'Number of Shares: 23' in response.data
    assert b'Purchase Price: $432.17' in response.data
    assert b'Purchase Date: April 23, 2019' in response.data
    assert b'canvas id="stockChart"' in response.data


def test_get_edit_stock_invalid_owner(test_client, stocks_blueprint_user_registration, stocks_blueprint_login_user2):
    """
    GIVEN a Flask application with a user logged in
    WHEN the '/stock/1' page is requested (GET) from a user that does NOT own the stock
    THEN check that a 403 error is returned
    """
    response = test_client.get('/stock/1', follow_redirects=True)
    print(response.data)
    assert response.status_code == 403
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Symbol: AAPL' not in response.data
    assert b"You don't have the permission to access the requested resource." in response.data


def test_get_stock_details_valid_owner_invalid_response(test_client, stocks_blueprint_user_login, mock_requests_get_failure):
    """
    GIVEN a Flask application with a user logged in
    WHEN the '/stock/1' page is requested (GET) from the user that owns that stock
    THEN check the response is valid
    """
    response = test_client.get('/stock/1', follow_redirects=True)
    print(response.data)
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Symbol: AAPL' in response.data
    assert b'Number of Shares: 23' in response.data
    assert b'Purchase Price: $432.17' in response.data
    assert b'Purchase Date: April 23, 2019' in response.data
    assert b'canvas id="stockChart"' not in response.data
