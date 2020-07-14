# Flask Stock Portfolio App

## Overview

This Flask application manages a stock portfolio for each user, including the user management aspects of a web application.

This project is developed as part of the *Learn Flask by Building and Deploying a Stock Portfolio App* course:

[https://testdriven.io/courses/learn-flask/](https://testdriven.io/courses/learn-flask/)

## Installation

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
(venv)$ pip install -r requirements.txt
```

Set the file that contains the Flask application and specify that the development environment should be used:

```sh
(venv)$ export FLASK_APP=app.py
(venv)$ export FLASK_ENV=development

(venv)$ export SECRET_KEY=<INSERT_SECRET_KEY>
(venv)$ export MAIL_USERNAME=<INSERT_EMAIL_ADDRESS>
(venv)$ export MAIL_PASSWORD=<INSERT_EMAIL_PASSWORD>
```

Run development server to serve the Flask application:

```sh
(venv)$ flask run
```

## Configuration

The following environment variables are configurable:

* SECRET_KEY - see description below
* CONFIG_TYPE - `config.DevelopmentConfig`, `config.ProductionConfig`, or `config.TestConfig`
* MAIL_USERNAME - email address used for sending emails from the app
* MAIL_PASSWORD - password for the email account sending emails from the app

## Key Python Modules Used

* Flask - framework for web application development
* Jinga - templating engine
* SQLAlchemy - ORM (Object Relational Mapper)
* Flask-Bcrypt - password hashing
* Flask-Login - support for user management
* Flask-Migrate - database migrations
* Flask-WTF - forms
* itsdangerous - helps with user management, especially tokens

This application is written using Python 3.8.

## Testing

The test suite for this project is written using [pytest](https://docs.pytest.org).

To run the full suite of tests:

```sh
(venv)$ pytest
```

### Test Coverage

The [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) package can be used to check the coverage of the tests:

```sh
(venv)$ pytest --cov=project
```
