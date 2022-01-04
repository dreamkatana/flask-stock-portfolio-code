## Overview

This Flask application manages a stock portfolio for each user, including the user management aspects of a web application.

This project is developed as part of the "Developing Web Applications with Python and Flask" course on [testdriven.io](https://testdriven.io/courses/learn-flask/):

* [https://testdriven.io/courses/learn-flask/](https://testdriven.io/courses/learn-flask/)

![Developing Web Applications with Python and Flask](project/static/img/learn_flask.png?raw=true "Developing Web Applications with Python and Flask")

## Website

[https://flask-stock-portfolio-app.herokuapp.com/](https://flask-stock-portfolio-app.herokuapp.com/)

## Installation Instructions

### Installation

Pull down the source code from this GitLab repository:

```sh
git clone git@gitlab.com:patkennedy79/flask-stock-portfolio-code.git
```

Create a new virtual environment:

```sh
$ cd flask-stock-portfolio-code
$ python3 -m venv venv
```

Activate the virtual environment:

```sh
$ source venv/bin/activate
```

Install the python packages specified in requirements.txt:

```sh
(venv) $ pip install -r requirements.txt
```

### Database Initialization

This Flask application needs a SQLite database to store data.  The database should be initialized via the Flask shell:

```
(venv) $ flask shell
>>> from project import database
>>> database.drop_all()
>>> database.create_all()
>>> quit()
(venv) $
```

### Running the Flask Application

Set the file that contains the Flask application and specify that the development environment should be used:

```sh
(venv) $ export FLASK_APP=app.py
(venv) $ export FLASK_ENV=development
```

Run development server to serve the Flask application:

```sh
(venv) $ flask run
```

Navigate to 'http://127.0.0.1:5000/' in your favorite web browser to view the website!

## Configuration

The following environment variables are recommended to be defined:

* SECRET_KEY - see description below
* CONFIG_TYPE - `config.DevelopmentConfig`, `config.ProductionConfig`, or `config.TestConfig`
* DATABASE_URL - URL for the database (either SQLite or Postgres)
* MAIL_USERNAME - username for the email account used for sending out emails from the app
* MAIL_PASSWORD - password for email account
* ALPHA_VANTAGE_API_KEY - API key for accessing Alpha Vantage service
* SENDGRID_API_KEY - API key for sending email via Sendgrid (production only!)

### Secret Key

The 'SECRET_KEY' can be generated using the following commands (assumes Python 3.6 or later):

```sh
(venv) $ python

>>> import secrets
>>> print(secrets.token_bytes(32))
>>> quit()

(venv) $ export SECRET_KEY=<secret_key_generated_in_interpreter>
```

NOTE: If working on Windows, use `set` instead of `export`.

### Alpha Vantage API Key

The Alpha Vantage API key is used to access the Alpha Vantage service to retrieve stock data.

In order to use the Alpha Vantage API, sign up for a free API key at:
[Alpha Vantage API Key](https://www.alphavantage.co/support/#api-key)

### SendGrid API Key

When running in production on Heroku, the SendGrid API key needs to be configured. Review chapter 40
(Deployment) on how to set up SendGrid and generate the API key.

## Key Python Modules Used

* **Flask**: micro-framework for web application development which includes the following dependencies:
  * click: package for creating command-line interfaces (CLI)
  * itsdangerous: cryptographically sign data 
  * Jinja2: templating engine
  * MarkupSafe: escapes characters so text is safe to use in HTML and XML
  * Werkzeug: set of utilities for creating a Python application that can talk to a WSGI server
* **pytest**: framework for testing Python projects
* **flake8**: static analysis tool
* **pytest-cov**: pytest extension for running coverage.py to check code coverage of tests
* **Flask-SQLAlchemy**: ORM (Object Relational Mapper) for Flask
* **Flask-Migrate**: relational database migration tool for Flask based on alembic
* **Flask-WTF**: simplifies forms in Flask
* **email_validator**: email syntax validation library for use with Flask-WTF
* **Flask-Login**: support for user management (login/logout) in Flask
* **Flask-Mail**: Flask extension for sending email
* **requests**: Python library for HTTP
* **freezegun**: library that allows your Python tests to travel through time by mocking the datetime module
* **Gunicorn**: 'Green Unicorn’ is a Python WSGI HTTP Server 

This application is written using Python 3.10.1.

## Testing

To run all the tests:

```sh
(venv) $ python -m pytest -v
```

To check the code coverage of the tests:

```sh
(venv) $ python -m pytest --cov-report term-missing --cov=project
```

**IMPORTANT**:
The following environment variables need to be configured in order for the tests to run successfully:

```sh
(venv) $ export MAIL_USERNAME=flaskstockportfolioapp@gmail.com
(venv) $ export MAIL_PASSWORD=test_password
```

NOTE: If working on Windows, use `set` instead of `export`.
