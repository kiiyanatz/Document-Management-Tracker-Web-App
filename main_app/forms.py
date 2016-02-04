from flask_wtf import Form
from wtforms.fields import TextField, PasswordField, \
    SubmitField, SelectField, FileField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional


class LoginForm(Form):
    email = TextField('Email', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Login')


class SignUpForm(Form):
    username = TextField('Username', [DataRequired(), Length(min=4, max=25)])
    email = TextField('Email', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired(), Length(
        min=4, max=25), EqualTo('cnf_pass', 'Passwords do not match')])
    cnf_pass = PasswordField('Confirm password', [DataRequired()])
    submit = SubmitField('Signup')


class FileUploadForm(Form):
    title = TextField(
        'Document title', [DataRequired(), Length(min=5, max=255)])
    link = TextField('Link', [Optional()])
    keywords = TextField('Keywords', [DataRequired()])
    department = SelectField(
        'Department', choices=[('Success', 'Success'),
                               ('Training', 'Training'),
                               ('Operations', 'Operations'),
                               ('Finance', 'Finance'),
                               ('Recruitment', 'Recruitment'),
                               ('Sales', 'Sales'),
                               ('Marketing', 'Marketing')
                               ])
    file_path = FileField('Your document')
    uploader = HiddenField()
    submit = SubmitField('Upload')


class SearchForm(Form):
    search_input = TextField('Search', [DataRequired()])
    submit = SubmitField()


class FilterForm(Form):
    department = SelectField(
        'Department', choices=[('Success', 'Success'),
                               ('Training', 'Training'),
                               ('Operations', 'Operations'),
                               ('Finance', 'Finance'),
                               ('Recruitment', 'Recruitment'),
                               ('Sales', 'Sales'),
                               ('Marketing', 'Marketing')
                               ])