from main_app import app
from flask import Flask, render_template, request, session, redirect
from .forms import LoginForm
from .forms import SignUpForm
from main_app import db
from main_app.models import User


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()

    input_username = ''
    input_password = ''

    if form.validate_on_submit():
        input_username = form.email.data
        input_password = form.password.data

        # Validate data for login

        return "Name is: " + input_username + " password is: " + input_password
    # Get database details
    #db_user = User.query.filter_by(username='kiiyanatz').all()
    return render_template('auth_views/signin.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Create database
        db.create_all()
        db.session.add(User(username, email, password))
        db.session.commit()

        return redirect('/')

    else:
        return render_template('auth_views/signup.html', form=form)
