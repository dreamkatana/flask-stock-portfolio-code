## Overview

This Flask application manages a stock portfolio for each user, including the user management aspects of a web application.

This project is developed as part of the "Developing Web Applications with Python and Flask" on [testdriven.io](https://testdriven.io/courses/learn-flask/).

## How to Run

In the top-level directory:

    $ export FLASK_APP=app.py
    $ export FLASK_ENV=development
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

## Key Python Modules Used

- Flask: micro-framework for web application development

This application is written using Python 3.8.5.

## Unit Testing

```sh
(venv) $ pytest -v
```
