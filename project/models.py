from project import database, bcrypt
from datetime import datetime
from flask import current_app
import requests


class Stock(database.Model):
    """
    Class that represents a purchased stock in a portfolio

    The following attributes of a stock are stored in this table:
        stock symbol
        number of shares
        purchase price
        purchase date (uses the `datetime` module)
        user ID - owner of the stock
        current price
        current price date (when data was retrieved from the Alpha Vantage API)
        position value = current price * number of shares
    """

    __tablename__ = 'stocks'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    symbol = database.Column(database.String, nullable=False)
    shares = database.Column(database.Integer, nullable=False)
    purchase_price = database.Column(database.Float, nullable=False)
    purchase_date = database.Column(database.DateTime, nullable=True)
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'))
    current_price = database.Column(database.Float, nullable=False)
    current_price_date = database.Column(database.DateTime, nullable=True)
    position_value = database.Column(database.Float, nullable=False)

    def __init__(self, stock_symbol, number_of_shares, purchase_price, purchase_date, user_id):
        self.symbol = stock_symbol
        self.shares = number_of_shares
        self.purchase_price = purchase_price
        self.purchase_date = purchase_date
        self.user_id = user_id
        self.current_price = 0.0
        self.current_price_date = None
        self.position_value = 0.0

    def __repr__(self):
        return f'<Stock: {self.symbol}>'

    def create_alpha_vantage_get_url_daily_compact(self):
        return 'https://www.alphavantage.co/query?function={}&symbol={}&outputsize={}&apikey={}'.format(
            'TIME_SERIES_DAILY_ADJUSTED',
            self.symbol,
            'compact',
            current_app.config['ALPHA_VANTAGE_API_KEY']
        )

    def get_stock_data(self):
        if self.current_price_date is None or self.current_price_date.date() != datetime.now().date():
            url = self.create_alpha_vantage_get_url_daily_compact()

            try:
                r = requests.get(url)
            except requests.exceptions.ConnectionError:
                return 'Error! Network problem preventing retrieving the stock data!'

            if r.status_code == 200:
                daily_data = r.json()

                for element in daily_data['Time Series (Daily)']:
                    current_price = float(daily_data['Time Series (Daily)'][element]['4. close'])
                    self.current_price = current_price
                    self.current_price_date = datetime.now()
                    self.position_value = round(current_price * self.shares, 2)
                    database.session.add(self)
                    break

        return ''

    def update_data(self, shares, purchase_price, purchase_date):
        self.shares = shares
        self.purchase_price = purchase_price
        self.purchase_date = purchase_date


class User(database.Model):
    """
    Class that represents a user of the application

    The following attributes of a user are stored in this table:
        * email - email address of the user
        * hashed password - hashed password (using Flask-Bcrypt)
        * authenticated - flag indicating if the user is currently logged in
        * registered_on - date & time that the user registered
        * email_confirmation_sent_on - date & time that the confirmation email was sent
        * email_confirmed - flag indicating if the user's email address has been confirmed
        * email_confirmed_on - date & time that the user's email address was confirmed

    REMEMBER: Never store the plaintext password in a database!
    """
    __tablename__ = 'users'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    email = database.Column(database.String, unique=True, nullable=False)
    password_hashed = database.Column(database.LargeBinary(60), nullable=False)
    authenticated = database.Column(database.Boolean, default=False)
    registered_on = database.Column(database.DateTime, nullable=True)
    email_confirmation_sent_on = database.Column(database.DateTime, nullable=True)
    email_confirmed = database.Column(database.Boolean, nullable=True, default=False)
    email_confirmed_on = database.Column(database.DateTime, nullable=True)
    recipes = database.relationship('Stock', backref='user', lazy='dynamic')

    def __init__(self, email, password_plaintext, email_confirmation_sent_on=None):
        self.email = email
        self.password_hashed = bcrypt.generate_password_hash(password_plaintext)
        self.authenticated = False
        self.registered_on = datetime.now()
        self.email_confirmation_sent_on = email_confirmation_sent_on
        self.email_confirmed = False
        self.email_confirmed_on = None

    def set_password(self, password_plaintext):
        self.password_hashed = bcrypt.generate_password_hash(password_plaintext)

    def is_password_correct(self, password_plaintext):
        return bcrypt.check_password_hash(self.password_hashed, password_plaintext)

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return str(self.id)

    def __repr__(self):
        return f'<User: {self.email}>'
