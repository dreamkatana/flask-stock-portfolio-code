"""
This file (test_users_routes.py) contains the unit tests for testing the
routes (routes.py) in the Users blueprint.
"""


def test_get_registration_page(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/register' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/register')
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'User Registration' in response.data
    assert b'Email:' in response.data
    assert b'Password:' in response.data


def test_valid_registration(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/register' page is posted to (POST) with valid data
    THEN check the response is valid and the user is created in
    """
    response = test_client.post('/register',
                                data=dict(email='patrick@email.com',
                                          password='FlaskIsAwesome123'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Thanks for registering, patrick@email.com!" in response.data
    assert b'Flask Stock Portfolio App' in response.data


def test_invalid_registration(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/register' page is posted to (POST) with invalid data
    THEN check an error message is returned to the user
    """
    response = test_client.post('/register',
                                data=dict(email='patrick2@email.com',
                                          password=''),   # Empty field is not allowed!
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Thanks for registering, patrick2@email.com!' not in response.data
    assert b'Flask Stock Portfolio App' in response.data
    assert b"[This field is required.]" in response.data


def test_duplicate_registration(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/register' page is posted to (POST) with data for an existing user
    THEN check an error message is returned to the user
    """
    test_client.post('/register',
                     data=dict(email='patrick@hotmail.com',
                               password='FlaskIsAwesome123'),
                     follow_redirects=True)
    response = test_client.post('/register',
                                data=dict(email='patrick@hotmail.com',   # Duplicate email address
                                          password='FlaskIsStillGreat!'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Thanks for registering, patrick@hotmail.com!' not in response.data
    assert b'Flask Stock Portfolio App' in response.data
    assert b'ERROR! Email (patrick@hotmail.com) already exists.' in response.data


def test_get_login_page(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Email" in response.data
    assert b"Password" in response.data


def test_valid_login_and_logout(test_client, init_database, register_default_user):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST) with valid credentials
    THEN check the response is valid
    """
    response = test_client.post('/login',
                                data=dict(email='patrick@gmail.com', password='FlaskIsAwesome123'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Thanks for logging in, patrick@gmail.com!" in response.data
    assert b'Flask Stock Portfolio App' in response.data

    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET) for a logged in user
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    print(response.data)
    assert response.status_code == 200
    assert b"Goodbye!" in response.data
    assert b'Flask Stock Portfolio App' in response.data


def test_invalid_login(test_client, init_database, register_default_user):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST) with invalid credentials (incorrect password)
    THEN check an error message is returned to the user
    """
    response = test_client.post('/login',
                                data=dict(email='patrick@gmail.com', password='FlaskIsNotAwesome'),
                                follow_redirects=True)
    assert response.status_code == 200
    print(response.data)
    assert b"ERROR! Incorrect login credentials." in response.data
    assert b'Flask Stock Portfolio App' in response.data


def test_valid_login_when_logged_in_already(test_client, init_database, register_default_user):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST) with value credentials for a user already logged in
    THEN check a warning is returned to the user
    """
    test_client.post('/login',
                     data=dict(email='patrick@gmail.com', password='FlaskIsAwesome123'),
                     follow_redirects=True)
    response = test_client.post('/login',
                                data=dict(email='patrick@gmail.com', password='FlaskIsAwesome123'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Already logged in!  Redirecting to your User Profile page...' in response.data
    assert b'Flask Stock Portfolio App' in response.data
    assert b'User Profile' in response.data


def test_invalid_logout(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/logout' page is posted to (POST)
    THEN check that a 405 error is returned
    """
    response = test_client.post('/logout', follow_redirects=True)
    assert response.status_code == 405
    assert b"Goodbye!" not in response.data
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Method Not Allowed' in response.data


def test_invalid_logout_not_logged_in(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET) when the user is not logged in
    THEN check that the user is redirected to the login page
    """
    test_client.get('/logout', follow_redirects=True)  # Double-check that there are no logged in users!
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Goodbye!" not in response.data
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Login' in response.data
    assert b'Please log in to access this page.' in response.data


def test_navigation_links_not_logged_in(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET) when the user is not logged in
    THEN check that the Register and Login links are present
    """
    test_client.get('/logout', follow_redirects=True)  # Double-check that there are no logged in users!
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Welcome to the Flask Stock Portfolio App!' in response.data
    assert b'Register' in response.data
    assert b'Login' in response.data
    assert b'Logout' not in response.data
    assert b'User Profile' not in response.data


def test_navigation_links_logged_in(test_client, init_database, log_in_user):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET) when the user is logged in
    THEN check that the Logout and User Profile links are present
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Welcome to the Flask Stock Portfolio App!' in response.data
    assert b'Register' not in response.data
    assert b'Login' not in response.data
    assert b'Logout' in response.data
    assert b'User Profile' in response.data


def test_user_profile_logged_in(test_client, init_database, log_in_user):
    """
    GIVEN a Flask application
    WHEN the '/user_profile' page is requested (GET) when the user is logged in
    THEN check that profile for the current user is presented
    """
    response = test_client.get('/user_profile')
    print(response.data)
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'User Profile' in response.data
    assert b'Email: patrick@gmail.com' in response.data


def test_user_profile_not_logged_in(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/user_profile' page is requested (GET) when the user is NOT logged in
    THEN check that the user is redirected to the login page
    """
    test_client.get('/logout', follow_redirects=True)  # Double-check that there are no logged in users!
    response = test_client.get('/user_profile', follow_redirects=True)
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'User Profile!' not in response.data
    assert b'Email: patrick@gmail.com' not in response.data
    assert b'Login' in response.data
    assert b'Please log in to access this page.' in response.data
