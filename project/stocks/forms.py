from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired


class AddStockForm(FlaskForm):
    symbol = StringField('Stock Symbol:', validators=[DataRequired()])
    shares = IntegerField('Number of Shares:', validators=[DataRequired()])
    price = DecimalField('Share Price:', validators=[DataRequired()])
    purchase_date_month = IntegerField('month ("mm"):', validators=[DataRequired()])
    purchase_date_day = IntegerField('day ("dd"):', validators=[DataRequired()])
    purchase_date_year = IntegerField('year ("yy"):', validators=[DataRequired()])
    submit = SubmitField('Add Stock')


class DeleteStock(FlaskForm):
    submit = SubmitField('Delete Stock')
