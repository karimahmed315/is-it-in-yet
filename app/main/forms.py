# is-it-in-yet/app/main/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL

class AlertForm(FlaskForm):
    """Form for users to add a new product alert."""
    product_url = StringField(
        'Product URL',
        validators=[
            DataRequired(message="Please enter a product URL."),
            URL(message="Please enter a valid URL.")
        ],
        render_kw={"placeholder": "https://www.amazon.co.uk/dp/B08H95Y452"}
    )
    submit = SubmitField('Add Alert')
