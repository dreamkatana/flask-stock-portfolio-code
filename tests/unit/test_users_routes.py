"""
This file (test_users_routes.py) contains the unit tests for testing the
routes (routes.py) in the Users blueprint.
"""
from project import mail
from project.models import User
from itsdangerous import URLSafeTimedSerializer
from flask import current_app


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
    assert b'Forgot your password?' in response.data
    assert b'Click Here to Reset!' in response.data


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
    assert b'Account Statistics' in response.data
    assert b'Joined on' in response.data
    assert b'Email address has not been confirmed!' in response.data
    assert b'Email address confirmed on' not in response.data
    assert b'Account Actions' in response.data
    assert b'Change Password' in response.data
    assert b'Resend Email Confirmation' in response.data


def test_user_profile_logged_in_email_confirmed(test_client, init_database, confirm_email_user):
    """
    GIVEN a Flask application
    WHEN the '/user_profile' page is requested (GET) when the user is logged in and their email address is confirmed
    THEN check that profile for the current user is presented
    """
    response = test_client.get('/user_profile')
    print(response.data)
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'User Profile' in response.data
    assert b'Email: patrick@gmail.com' in response.data
    assert b'Account Statistics' in response.data
    assert b'Joined on' in response.data
    assert b'Email address has not been confirmed!' not in response.data
    assert b'Email address confirmed on Tuesday, March 10, 2020' in response.data
    assert b'Account Actions' in response.data
    assert b'Change Password' in response.data
    assert b'Resend Email Confirmation' not in response.data


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


def test_user_registration_email(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/register' page is posted to (POST) with valid data
    THEN check that an email was queued up to send
    """
    with mail.record_messages() as outbox:
        response = test_client.post('/register',
                                    data=dict(email='patrick@yahoo.com',
                                              password='FlaskIsAwesome123'),
                                    follow_redirects=True)
        assert response.status_code == 200
        assert len(outbox) == 1
        assert outbox[0].subject == 'Flask Stock Portfolio App - Confirm Your Email Address'
        assert outbox[0].sender == 'flaskstockportfolioapp@gmail.com'
        assert outbox[0].recipients[0] == 'patrick@yahoo.com'
        assert 'Questions? Comments? Email flaskstockportfolioapp@gmail.com' in outbox[0].html
        assert 'http://localhost/confirm/' in outbox[0].html


def test_confirm_email_valid(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/confirm/<token>' page is posted to (POST) with valid data
    THEN check that the user's email address is marked as confirmed
    """
    url_link_formatted = ''

    with mail.record_messages() as outbox:
        response = test_client.post('/register',
                                    data=dict(email='patrick@emailserver.com',
                                              password='FlaskIsSuper456'),
                                    follow_redirects=True)
        assert response.status_code == 200
        assert len(outbox) == 1
        email_html = outbox[0].html

        for line in email_html.splitlines():
            if 'localhost/confirm' in line:
                url_link = line
                print(f'Found line: {url_link}')

        # Display the print statement above to get an example of what the line
        # with the URL link looks like
        # Strip off the '<a href="http://localhost' from the url_link
        url_link_formatted = url_link[25:103]
        print(f'url_link_formatted: {url_link_formatted}')

    response = test_client.get(url_link_formatted, follow_redirects=True)
    print(response.data)
    assert response.status_code == 200
    user = User.query.filter_by(email='patrick@emailserver.com').first()
    assert user.email_confirmed

    """
    GIVEN a Flask application
    WHEN the '/confirm/<token>' page is posted to (POST) with valid data
         but the user's email is already confirmed
    THEN check that the user's email address is marked as confirmed
    """
    response = test_client.get(url_link_formatted, follow_redirects=True)
    print(response.data)
    assert response.status_code == 200
    user = User.query.filter_by(email='patrick@emailserver.com').first()
    assert user.email_confirmed
    assert b'Account already confirmed.' in response.data


def test_confirm_email_invalid(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/confirm/<token>' page is posted to (POST) with invalid data
    THEN check that the user's email address is marked as confirmed
    """
    response = test_client.get('/confirm/bad_confirmation_link', follow_redirects=True)
    print(response.data)
    assert response.status_code == 200
    assert b'The confirmation link is invalid or has expired.' in response.data


def test_get_password_reset_via_email_page(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/password_reset_via_email' page is requested (GET)
    THEN check that the page is successfully returned
    """
    response = test_client.get('/password_reset_via_email', follow_redirects=True)
    print(response.data)
    assert response.status_code == 200
    assert b'Password Reset via Email' in response.data
    assert b'Email:' in response.data
    assert b'Submit' in response.data


def test_post_password_reset_via_email_page_valid(test_client, confirm_email_user):
    """
    GIVEN a Flask application
    WHEN the '/password_reset_via_email' page is posted to (POST) with a valid email address
    THEN check that an email was queued up to send
    """
    with mail.record_messages() as outbox:
        response = test_client.post('/password_reset_via_email',
                                    data=dict(email='patrick@gmail.com'),
                                    follow_redirects=True)
        assert response.status_code == 200
        assert b'Please check your email for a password reset link.' in response.data
        assert len(outbox) == 1
        assert outbox[0].subject == 'Flask Stock Portfolio App - Password Reset Requested'
        assert outbox[0].sender == 'flaskstockportfolioapp@gmail.com'
        assert outbox[0].recipients[0] == 'patrick@gmail.com'
        assert 'Questions? Comments? Email flaskstockportfolioapp@gmail.com' in outbox[0].html
        assert 'http://localhost/password_reset_via_token/' in outbox[0].html


def test_post_password_reset_via_email_page_invalid(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/password_reset_via_email' page is posted to (POST) with an invalid email address
    THEN check that an error message is flashed
    """
    with mail.record_messages() as outbox:
        response = test_client.post('/password_reset_via_email',
                                    data=dict(email='notpatrick@gmail.com'),
                                    follow_redirects=True)
        assert response.status_code == 200
        print(response.data)
        assert len(outbox) == 0
        assert b'Error! Invalid email address!' in response.data


def test_post_password_reset_via_email_page_not_confirmed(test_client, init_database, log_in_user):
    """
    GIVEN a Flask application
    WHEN the '/password_reset_via_email' page is posted to (POST) with a email address that has not been confirmed
    THEN check that an error message is flashed
    """
    with mail.record_messages() as outbox:
        response = test_client.post('/password_reset_via_email',
                                    data=dict(email='patrick@gmail.com'),
                                    follow_redirects=True)
        assert response.status_code == 200
        assert len(outbox) == 0
        assert b'Your email address must be confirmed before attempting a password reset.' in response.data


def test_get_password_reset_valid_token(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/password_reset_via_email/<token>' page is requested (GET) with a valid token
    THEN check that the page is successfully returned
    """
    password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = password_reset_serializer.dumps('patrick@gmail.com', salt='password-reset-salt')
    response = test_client.get('/password_reset_via_token/' + token, follow_redirects=True)
    assert response.status_code == 200
    assert b'Password Reset:' in response.data
    assert b'New Password:' in response.data
    assert b'Submit' in response.data


def test_get_password_reset_invalid_token(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/password_reset_via_email/<token>' page is requested (GET) with an invalid token
    THEN check that the page is successfully returned
    """
    token = 'invalid_token'
    response = test_client.get('/password_reset_via_token/' + token, follow_redirects=True)
    assert response.status_code == 200
    assert b'Password Reset:' not in response.data
    assert b'The password reset link is invalid or has expired.' in response.data


def test_post_password_reset_valid_token(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/password_reset_via_email/<token>' page is posted to (POST) with a valid token
    THEN check that the password provided is processed
    """
    password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = password_reset_serializer.dumps('patrick@gmail.com', salt='password-reset-salt')
    response = test_client.post('/password_reset_via_token/' + token,
                                data=dict(password='FlaskIsAwesome123'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Your password has been updated!' in response.data


def test_post_password_reset_invalid_token(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/password_reset_via_email/<token>' page is posted to (POST) with a invalid token
    THEN check that the password provided is processed
    """
    token = 'invalid_token'
    response = test_client.post('/password_reset_via_token/' + token,
                                data=dict(password='FlaskIsStillGreat45678'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Your password has been updated!' not in response.data
    assert b'The password reset link is invalid or has expired.' in response.data


def test_get_change_password_logged_in(test_client, init_database, log_in_user):
    """
    GIVEN a Flask application with the user logged in
    WHEN the '/password_change' page is retrieved (GET)
    THEN check that the page is retrieved successfully
    """
    response = test_client.get('/password_change', follow_redirects=True)
    assert response.status_code == 200
    assert b'Password Change' in response.data
    assert b'New Password:' in response.data


def test_get_change_password_not_logged_in(test_client, init_database):
    """
    GIVEN a Flask application with the user not logged in
    WHEN the '/password_change' page is retrieved (GET)
    THEN check that an error message is flashed
    """
    response = test_client.get('/password_change', follow_redirects=True)
    assert response.status_code == 200
    assert b'Password Change' not in response.data
    assert b'New Password:' not in response.data
    assert b'Please log in to access this page.' in response.data


def test_post_change_password_logged_in(test_client, init_database, log_in_user):
    """
    GIVEN a Flask application with the user logged in
    WHEN the '/password_change' page is posted to (POST) with valid data
    THEN check that the page is retrieved successfully
    """
    response = test_client.post('/password_change',
                                data=dict(password='FlaskIsTheBest987'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Password has been updated!' in response.data


def test_post_change_password_not_logged_in(test_client, init_database):
    """
    GIVEN a Flask application with the user not logged in
    WHEN the '/password_change' page is posted to (POST) with valid data
    THEN check that the page is retrieved successfully
    """
    response = test_client.post('/password_change',
                                data=dict(password='FlaskIsTheBest987'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Password has been updated!' not in response.data
    assert b'Please log in to access this page.' in response.data
