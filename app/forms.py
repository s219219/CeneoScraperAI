from wtforms import StringField, SubmitField, validators
from flask_wtf import FlaskForm
class ProductForm(FlaskForm):
    productId = StringField(
        'Enter product Id',
        [
            validators.DataRequired(message = "Product Id must be given"),
            validators.Length(min=8, max=8, message= "Product Id must have 8 characters"),
            validators.Regexp(regex="^[0-9]+$", message="Product Id can contain only digits")
        ]) 
    submit = SubmitField('Extract')
