from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    mobile_number = StringField('Mobile Number', validators=[DataRequired()])
    submit = SubmitField('Login')
