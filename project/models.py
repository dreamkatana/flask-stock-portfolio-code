from project import database
from project import bcrypt
from datetime import datetime


class Stock(database.Model):
    """
    Class that represents a purchased stock in a portfolio

    The following attributes of a stock are stored in this table:
        stock symbol
        number of shares
        share price (at purchase)
    """

    __tablename__ = 'stocks'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    symbol = database.Column(database.String, nullable=False)
    shares = database.Column(database.Integer, nullable=False)
    price = database.Column(database.Float, nullable=False)

    def __init__(self, stock_symbol, number_of_shares, purchase_price):
        self.symbol = stock_symbol
        self.shares = number_of_shares
        self.price = purchase_price


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
