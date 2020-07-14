## Overview

This Flask application manages a stock portfolio for each user, including the user management aspects of a web application.

This project is developed as part of the "Learn Flask by Building and Deplying a Stock Portfolio App" on [testdriven.io](https://testdriven.io/courses/).

## How to Run

Start by setting the necessary configuration variables:

    $ export FLASK_APP=app.py
    $ export FLASK_ENV=development

    $ export SECRET_KEY=<INSERT_SECRET_KEY>
    $ export MAIL_USERNAME=<INSERT_EMAIL_ADDRESS>
    $ export MAIL_PASSWORD=<INSERT_EMAIL_PASSWORD>

Run the Flask Development Server:

    $ flask run

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

The following environment variables are configurable:

* SECRET_KEY - see description below
* CONFIG_TYPE - `config.DevelopmentConfig`, `config.ProductionConfig`, or `config.TestConfig`

## Key Python Modules Used

- Flask: micro-framework for web application development

This application is written using Python 3.8.

## Unit Testing

```sh
(venv) $ python -m pytest -v
```
