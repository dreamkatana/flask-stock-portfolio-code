from project import database
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask import current_app
import flask_login
import requests


# ----------------
# Helper Functions
# ----------------

def create_alpha_vantage_url_quote(symbol: str) -> str:
    return 'https://www.alphavantage.co/query?function={}&symbol={}&apikey={}'.format(
        'GLOBAL_QUOTE',
        symbol,
        current_app.config['ALPHA_VANTAGE_API_KEY']
    )


def get_current_stock_price(symbol: str) -> float:
    url = create_alpha_vantage_url_quote(symbol)

    # Attempt the GET call to Alpha Vantage and check that a ConnectionError does
    # not occur, which happens when the GET call fails due to a network issue
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        current_app.logger.error(
            f'Error! Network problem preventing retrieving the stock data ({symbol})!')

    # Status code returned from Alpha Vantage needs to be 200 (OK) to process stock data
    if r.status_code != 200:
        current_app.logger.warning(f'Error! Received unexpected status code ({r.status_code}) '
                                   f'when retrieving daily stock data ({symbol})!')
        return 0.0

    stock_data = r.json()

    # The key of 'Global Quote' needs to be present in order to process the stock data.
    # Typically, this key will not be present if the API rate limit has been exceeded.
    if 'Global Quote' not in stock_data:
        current_app.logger.warning(f'Could not find the Global Quote key when retrieving '
                                   f'the daily stock data ({symbol})!')
        return 0.0

    return float(stock_data['Global Quote']['05. price'])


def create_alpha_vantage_get_url_weekly(symbol: str) -> str:
    return 'https://www.alphavantage.co/query?function={}&symbol={}&apikey={}'.format(
        'TIME_SERIES_WEEKLY_ADJUSTED',
        symbol,
        current_app.config['ALPHA_VANTAGE_API_KEY']
    )


# ---------------
# Database Models
# ---------------

class Stock(database.Model):
    """
    Class that represents a purchased stock in a portfolio.

    The following attributes of a stock are stored in this table:
        stock symbol (type: string)
        number of shares (type: integer)
        purchase price (type: integer)
        primary key of User that owns the stock (type: integer)
        purchase date (type: datetime)
        current price (type: integer)
        date when current price was retrieved from the Alpha Vantage API (type: datetime)
        position value = current price * number of shares (type: integer)

    Note: Due to a limitation in the data types supported by SQLite, the
          purchase price, current price, and position value are stored as integers:
              $24.10 -> 2410
              $100.00 -> 10000
              $87.65 -> 8765
    """

    __tablename__ = 'stocks'

    id = mapped_column(Integer(), primary_key=True)
    stock_symbol = mapped_column(String())
    number_of_shares = mapped_column(Integer())
    purchase_price = mapped_column(Integer())
    user_id = mapped_column(ForeignKey('users.id'))
    purchase_date = mapped_column(DateTime())
    current_price = mapped_column(Integer())
    current_price_date = mapped_column(DateTime())
    position_value = mapped_column(Integer())

    # Define the relationship to the `User` class
    user_relationship = relationship('User', back_populates='stocks_relationship')

    def __init__(self, stock_symbol: str, number_of_shares: str, purchase_price: str,
                 user_id: int, purchase_date=None):
        self.stock_symbol = stock_symbol
        self.number_of_shares = int(number_of_shares)
        self.purchase_price = int(float(purchase_price) * 100)
        self.user_id = user_id
        self.purchase_date = purchase_date
        self.current_price = 0
        self.current_price_date = None
        self.position_value = 0

    def __repr__(self):
        return f'{self.stock_symbol} - {self.number_of_shares} shares purchased at ${self.purchase_price / 100}'

    def get_stock_data(self):
        if self.current_price_date is None or self.current_price_date.date() != datetime.now().date():
            current_price = get_current_stock_price(self.stock_symbol)
            if current_price > 0.0:
                self.current_price = int(current_price * 100)
                self.current_price_date = datetime.now()
                self.position_value = self.current_price * self.number_of_shares
                current_app.logger.debug(f'Retrieved current price {self.current_price / 100} '
                                         f'for the stock data ({self.stock_symbol})!')

    def get_stock_position_value(self) -> float:
        return float(self.position_value / 100)

    def get_weekly_stock_data(self):
        title = 'Stock chart is unavailable.'
        labels = []
        values = []
        url = create_alpha_vantage_get_url_weekly(self.stock_symbol)

        try:
            r = requests.get(url)
        except requests.exceptions.ConnectionError:
            current_app.logger.info(
                f'Error! Network problem preventing retrieving the weekly stock data ({self.stock_symbol})!')

        # Status code returned from Alpha Vantage needs to be 200 (OK) to process stock data
        if r.status_code != 200:
            current_app.logger.warning(f'Error! Received unexpected status code ({r.status_code}) '
                                       f'when retrieving weekly stock data ({self.stock_symbol})!')
            return title, '', ''

        weekly_data = r.json()

        # The key of 'Weekly Adjusted Time Series' needs to be present in order to process the stock data
        # Typically, this key will not be present if the API rate limit has been exceeded.
        if 'Weekly Adjusted Time Series' not in weekly_data:
            current_app.logger.warning(f'Could not find the Weekly Adjusted Time Series key when retrieving '
                                       f'the weekly stock data ({self.stock_symbol})!')
            return title, '', ''

        title = f'Weekly Prices ({self.stock_symbol})'

        # Determine the start date as either:
        #   - If the start date is less than 12 weeks ago, then use the date from 12 weeks ago
        #   - Otherwise, use the purchase date
        start_date = self.purchase_date
        if (datetime.now() - self.purchase_date) < timedelta(weeks=12):
            start_date = datetime.now() - timedelta(weeks=12)

        for element in weekly_data['Weekly Adjusted Time Series']:
            date = datetime.fromisoformat(element)
            if date.date() > start_date.date():
                labels.append(date)
                values.append(weekly_data['Weekly Adjusted Time Series'][element]['4. close'])

        # Reverse the elements as the data from Alpha Vantage is read in latest to oldest
        labels.reverse()
        values.reverse()

        return title, labels, values

    def update(self, number_of_shares='', purchase_price='', purchase_date=None):
        if number_of_shares:
            self.number_of_shares = int(number_of_shares)
            self.position_value = self.current_price * self.number_of_shares

        if purchase_price:
            self.purchase_price = int(float(purchase_price) * 100)

        if purchase_date:
            self.purchase_date = purchase_date


class User(flask_login.UserMixin, database.Model):
    """
    Class that represents a user of the application

    The following attributes of a user are stored in this table:
        * email - email address of the user
        * hashed password - hashed password (using werkzeug.security)
        * registered_on - date & time that the user registered
        * email_confirmation_sent_on - date & time that the confirmation email was sent
        * email_confirmed - flag indicating if the user's email address has been confirmed
        * email_confirmed_on - date & time that the user's email address was confirmed

    REMEMBER: Never store the plaintext password in a database!
    """
    __tablename__ = 'users'

    id = mapped_column(Integer(), primary_key=True)
    email = mapped_column(String(), unique=True)
    password_hashed = mapped_column(String(255))
    registered_on = mapped_column(DateTime())
    email_confirmation_sent_on = mapped_column(DateTime())
    email_confirmed = mapped_column(Boolean(), default=False)
    email_confirmed_on = mapped_column(DateTime())
    user_type = mapped_column(String(10), default='User')

    # Define the relationship to the `Stock` class
    stocks_relationship = relationship('Stock', back_populates='user_relationship')

    # Define the relationship to the `WatchStock` class
    watchstocks_relationship = relationship('WatchStock', back_populates='user_relationship')

    def __init__(self, email: str, password_plaintext: str, user_type='User'):
        """Create a new User object

        This constructor assumes that an email is sent to the new user to confirm
        their email address at the same time that the user is registered.
        """
        self.email = email
        self.password_hashed = self._generate_password_hash(password_plaintext)
        self.registered_on = datetime.now()
        self.email_confirmation_sent_on = datetime.now()
        self.email_confirmed = False
        self.email_confirmed_on = None
        self.user_type = user_type

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password_hashed, password_plaintext)

    def set_password(self, password_plaintext: str):
        self.password_hashed = self._generate_password_hash(password_plaintext)

    @staticmethod
    def _generate_password_hash(password_plaintext):
        return generate_password_hash(password_plaintext)

    def __repr__(self):
        return f'<User: {self.email}>'

    def is_admin(self):
        return self.user_type == 'Admin'

    def confirm_email_address(self):
        self.email_confirmed = True
        self.email_confirmed_on = datetime.now()

    def unconfirm_email_address(self):
        self.email_confirmed = False
        self.email_confirmed_on = None


class WatchStock(database.Model):
    """
    Class that represents a stock in a watch list.

    The following attributes of a stock are stored in this table:
        stock symbol (type: string)
        company name (type: string)
        current share price (type: integer)
        date when current price was retrieved from the Alpha Vantage API (type: datetime)
        52-week low (type: integer)
        52-week high (type: integer)
        market cap (type: string)
        dividend per share (type: integer)
        p/e ratio (type: integer)
        peg ratio (type: integer)
        profit margin (type: integer)
        beta (type: integer)
        price-to-book ratio (type: integer)
        date when stock data was retrieved from the Alpha Vantage API (type: datetime)
        primary key of User that owns the watchstock (type: integer)

    Note: Due to a limitation in the data types supported by SQLite, the
          attributes displayed as floating point values are stored as integers:
              $24.10 -> 2410
              $100.00 -> 10000
              $87.65 -> 8765
              12.84% -> 1284
    """

    __tablename__ = 'watchstocks'

    id = mapped_column(Integer(), primary_key=True)
    stock_symbol = mapped_column(String(), nullable=False)
    company_name = mapped_column(String())
    current_share_price = mapped_column(Integer())
    current_share_price_date = mapped_column(DateTime())
    fiftytwo_week_low = mapped_column(Integer())
    fiftytwo_week_high = mapped_column(Integer())
    market_cap = mapped_column(String())
    dividend_per_share = mapped_column(Integer())
    pe_ratio = mapped_column(Integer())
    peg_ratio = mapped_column(Integer())
    profit_margin = mapped_column(Integer())
    beta = mapped_column(Integer())
    price_to_book_ratio = mapped_column(Integer())
    stock_data_date = mapped_column(DateTime())
    user_id = mapped_column(ForeignKey('users.id'))

    # Define the relationship to the `User` class
    user_relationship = relationship('User', back_populates='watchstocks_relationship')

    def __init__(self, stock_symbol: str, user_id: str):
        self.stock_symbol = stock_symbol
        self.company_name = None
        self.current_share_price = 0
        self.current_share_price_date = None
        self.fiftytwo_week_low = 0
        self.fiftytwo_week_high = 0
        self.market_cap = None
        self.dividend_per_share = 0
        self.pe_ratio = 0
        self.peg_ratio = 0
        self.profit_margin = 0
        self.beta = 0
        self.price_to_book_ratio = 0
        self.stock_data_date = None
        self.user_id = user_id

    def __repr__(self):
        return f'{self.stock_symbol}'

    def retrieve_current_share_price(self):
        if self.current_share_price_date is None or self.current_share_price_date.date() != datetime.now().date():
            current_price = get_current_stock_price(self.stock_symbol)
            if current_price > 0.0:
                self.current_share_price = int(current_price * 100)
                self.current_share_price_date = datetime.now()
                current_app.logger.info(f'Retrieved current price {self.current_share_price / 100} '
                                        f'for {self.stock_symbol}!')

    def create_alpha_vantage_url_overview(self):
        return 'https://www.alphavantage.co/query?function={}&symbol={}&apikey={}'.format(
            'OVERVIEW',
            self.stock_symbol,
            current_app.config['ALPHA_VANTAGE_API_KEY']
        )

    def retrieve_stock_analysis_data(self):
        # If the stock analysis data has already been retrieved for the current day, then the
        # data is still valid and there is no need to retrieve it again
        if self.stock_data_date is not None and self.stock_data_date.date() == datetime.now().date():
            current_app.logger.info(f'Valid stock analysis data for {self.stock_symbol} '
                                    f'already exists ({self.stock_data_date}).')
            return

        # Attempt the GET call to Alpha Vantage and check that a ConnectionError does
        # not occur, which happens when the GET call fails due to a network issue
        try:
            url = self.create_alpha_vantage_url_overview()
            r = requests.get(url)
        except requests.exceptions.ConnectionError:
            current_app.logger.error(
                f'Error! Network problem preventing retrieving the stock analysis data ({self.stock_symbol})!')

        # Status code returned from Alpha Vantage needs to be 200 (OK) to process stock data
        if r.status_code != 200:
            current_app.logger.warning(f'Error! Received unexpected status code ({r.status_code}) '
                                       f'when retrieving stock analysis data ({self.stock_symbol})!')
            return

        data = r.json()

        # The key of 'AssetType' needs to be present in order to confirm that valid data is available.
        # Typically, this key will not be present if the API rate limit has been exceeded.
        if 'AssetType' not in data:
            current_app.logger.warning(f'Could not find valid data when retrieving '
                                       f'the stock analysis data ({self.stock_symbol})!')
            return

        self.company_name = data['Name']
        self.fiftytwo_week_low = self.parse_input_string_integer(data['52WeekLow'])
        self.fiftytwo_week_high = self.parse_input_string_integer(data['52WeekHigh'])
        self.market_cap = data['MarketCapitalization']
        self.dividend_per_share = self.parse_input_string_integer(data['DividendPerShare'])
        self.pe_ratio = self.parse_input_string_integer(data['PERatio'])
        self.peg_ratio = self.parse_input_string_integer(data['PEGRatio'])
        self.profit_margin = self.parse_input_string_percentage(data['ProfitMargin'])
        self.beta = self.parse_input_string_integer(data['Beta'])
        self.price_to_book_ratio = self.parse_input_string_integer(data['PriceToBookRatio'])
        self.stock_data_date = datetime.now()
        current_app.logger.info(f'Retrieved valid stock analysis data for {self.stock_symbol} '
                                f'at time {self.stock_data_date}.')

    @staticmethod
    def parse_input_string_integer(input_field: str) -> int:
        if input_field == 'None' or input_field == '' or input_field == '-':
            return 0

        return int(float(input_field) * 100)

    @staticmethod
    def parse_input_string_percentage(input_field: str) -> int:
        if input_field == 'None' or input_field == '':
            return 0

        return int(float(input_field) * 10000)

    def get_current_share_price(self) -> float:
        return self.current_share_price / 100

    def get_fiftytwo_week_low(self) -> float:
        return self.fiftytwo_week_low / 100

    def get_fiftytwo_week_high(self) -> float:
        return self.fiftytwo_week_high / 100

    def get_market_cap(self) -> str:
        if self.market_cap is None:
            return '-'

        market_cap_integer = int(self.market_cap)
        market_cap_integer_billions = market_cap_integer / 1_000_000_000
        return str(round(market_cap_integer_billions, 1)) + 'B'

    def get_dividend_per_share(self) -> float:
        return self.dividend_per_share / 100

    def get_pe_ratio(self) -> float:
        return self.pe_ratio / 100

    def get_peg_ratio(self) -> float:
        if self.pe_ratio < 0.1:
            return 0.0
        return self.peg_ratio / 100

    def get_profit_margin(self) -> float:
        return self.profit_margin / 100

    def get_beta(self) -> float:
        return self.beta / 100

    def get_price_to_book_ratio(self) -> float:
        if self.price_to_book_ratio is None:
            return 0.0
        return self.price_to_book_ratio / 100
