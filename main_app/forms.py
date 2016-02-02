from flask_wtf import Form
from wtforms.fields import TextField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(Form):
    email = TextField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class SignUpForm(Form):
	username = TextField('Username', validators=[DataRequired()])
	email = TextField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Signup')