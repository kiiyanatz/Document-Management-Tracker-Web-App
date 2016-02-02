from flask_wtf import Form
from wtforms.fields import TextField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(Form):
    email = TextField('Email', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Login')


class SignUpForm(Form):
	username = TextField('Username', [DataRequired(), Length(min=4, max=25)])
	email = TextField('Email', [DataRequired(), Email()])
	password = PasswordField('Password', [DataRequired(), Length(min=4, max=25), EqualTo('cnf_pass', 'Passwords do not match')])
	cnf_pass = PasswordField('Confirm password', [DataRequired()])
	submit = SubmitField('Signup')