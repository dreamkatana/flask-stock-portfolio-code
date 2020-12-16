## Overview

This Flask application manages a stock portfolio for each user, including the user management aspects of a web application.

This project is developed as part of the "Developing Web Applications with Python and Flask" course on [testdriven.io](https://testdriven.io/courses/learn-flask/):

* [https://testdriven.io/courses/learn-flask/](https://testdriven.io/courses/learn-flask/)

## How to Run

In the top-level directory:

```sh
$ export FLASK_APP=app.py
$ export FLASK_ENV=development
$ flask run
```

## Installation Instructions

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

Install the python packages in requirements.txt:

```sh
(venv) $ pip install -r requirements.txt
```

Set the file that contains the Flask application and specify that the development environment should be used:

```sh
(venv) $ export FLASK_APP=app.py
(venv) $ export FLASK_ENV=development
```

Run development server to serve the Flask application:

```sh
(venv) $ flask run
```

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

- Flask: micro-framework for web application development
- pytest: framework for testing Python projects
* SQLAlchemy - ORM (Object Relational Mapper)
* Flask-Bcrypt - password hashing
* Flask-Login - support for user management
* Flask-Migrate - database migrations
* Flask-WTF - forms
* itsdangerous - helps with user management, especially tokens

This application is written using Python 3.9.0.

## Unit Testing

To run all the tests:

```sh
(venv) $ pytest -v
```

To check the code coverage of the tests:

```sh
(venv) $ pytest --cov-report term-missing --cov=project
```
