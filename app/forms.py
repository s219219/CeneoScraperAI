from wtforms import Form, StringField, SubmitField, validators

class ProductForm(Form):
    productId = StringField(
        'Enter product Id',
        [
            validators.DataRequired(message = "Product Id must be given"),
            validators.Length(min=8, max=8, message= "Product Id must have 8 characters"),
            validators.Regexp(regex="^[0-9]+$", message="Product Id can contain only digits")
        ]) 
    submit = SubmitField('Extract')
