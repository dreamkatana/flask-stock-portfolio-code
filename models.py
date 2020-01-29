from app import database


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
