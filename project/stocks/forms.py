from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired


class AddStockForm(FlaskForm):
    symbol = StringField('Stock Symbol:', validators=[DataRequired()])
    shares = IntegerField('Number of Shares:', validators=[DataRequired()])
    price = DecimalField('Share Price:', validators=[DataRequired()])
    submit = SubmitField('Add Stock')
