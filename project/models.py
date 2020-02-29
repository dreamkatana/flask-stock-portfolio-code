from project import database
from project import bcrypt


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
        email
        hashed password

    REMEMBER: Never store the plaintext password in a database!
    """
    __tablename__ = 'users'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    email = database.Column(database.String, unique=True, nullable=False)
    password_hashed = database.Column(database.LargeBinary(60), nullable=False)

    def __init__(self, email, password_plaintext):
        self.email = email
        self.password_hashed = bcrypt.generate_password_hash(password_plaintext)

    # def set_password(self, password_plaintext):
    #     self.password_hashed = bcrypt.generate_password_hash(password_plaintext)
    #
    # def is_password_correct(self, password_plaintext):
    #     return bcrypt.check_password_hash(self.password_hashed, password_plaintext)

    def __repr__(self):
        return f'<User: {self.email}>'
