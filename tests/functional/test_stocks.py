"""
This file (test_stocks.py) contains the functional tests for testing the Stocks blueprint.
"""
import requests


########################
#### Helper Classes ####
########################

class MockSuccessResponse(object):
    def __init__(self, url):
        self.status_code = 200
        self.url = url
        self.headers = {'blaa': '1234'}

    def json(self):
        return {
            'Meta Data': {
                "2. Symbol": "MSFT",
                "3. Last Refreshed": "2020-03-24"
            },
            'Time Series (Daily)': {
                "2020-03-24": {
                    "4. close": "148.3400",
                },
                "2020-03-23": {
                    "4. close": "135.9800",
                }
            }
        }


class MockFailedResponse(object):
    def __init__(self, url):
        self.status_code = 404
        self.url = url
        self.headers = {'blaa': '1234'}

    def json(self):
        return {'error': 'bad'}


##########################
#### Functional Tests ####
##########################

def test_monkeypatch_get_success(monkeypatch):
    """
    GIVEN a Flask application and a monkeypatched version of requests.get()
    WHEN the HTTP response is set to successful
    THEN check the HTTP response
    """
    def mock_get(url):
        return MockSuccessResponse(url)

    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=MSFT&apikey=demo'
    monkeypatch.setattr(requests, 'get', mock_get)
    r = requests.get(url)
    assert r.status_code == 200
    assert r.url == url
    assert 'MSFT' in r.json()['Meta Data']['2. Symbol']
    assert '2020-03-24' in r.json()['Meta Data']['3. Last Refreshed']
    assert '148.34' in r.json()['Time Series (Daily)']['2020-03-24']['4. close']


def test_monkeypatch_get_failure(monkeypatch):
    """
    GIVEN a Flask application and a monkeypatched version of requests.get()
    WHEN the HTTP response is set to failed
    THEN check the HTTP response
    """
    def mock_get(url):
        return MockFailedResponse(url)

    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=MSFT&apikey=demo'
    monkeypatch.setattr(requests, 'get', mock_get)
    r = requests.get(url)
    print(r.json())
    assert r.status_code == 404
    assert r.url == url
    assert 'bad' in r.json()['error']
