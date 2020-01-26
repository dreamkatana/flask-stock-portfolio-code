"""
This file (test_app.py) contains the unit tests for the app.py file.
"""
import pytest
from app import app


def test_index_page():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert b'Flask Stock Portfolio App' in response.data
        assert b'Welcome to the Flask Stock Portfolio App!' in response.data


def test_about_page():
    with app.test_client() as client:
        response = client.get('/about')
        assert b'Flask Stock Portfolio App' in response.data
        assert b'About' in response.data
        assert b'This application is built using the Flask web framework.' in response.data
        assert b'Course developed by TestDriven.io.' in response.data


def test_get_add_stock_page():
    with app.test_client() as client:
        response = client.get('/add_stock')
        assert b'Flask Stock Portfolio App' in response.data
        assert b'Add a Stock:' in response.data
        assert b'Stock Symbol:' in response.data
        assert b'Number of Shares:' in response.data
        assert b'Share Price:' in response.data


def test_post_add_stock_page():
    with app.test_client() as client:
        response = client.post('/add_stock',
                         data=dict(stockSymbol='AAPL',
                                   numberOfShares='23',
                                   sharePrice='432.17'),
                         follow_redirects=True)
        assert response.status_code == 200
        assert b'List of Stocks:' in response.data
        assert b'Stock Symbol' in response.data
        assert b'Number of Shares' in response.data
        assert b'Share Price' in response.data
