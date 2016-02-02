from main_app import app
from flask import Flask, render_template, request, session, redirect
from .forms import LoginForm
from .forms import SignUpForm
from main_app import db
from main_app.models import User
from werkzeug.security import check_password_hash, generate_password_hash

@app.route('/')
def home():
    if session['logged_in'] == True:
        db_users = User.query.all()
        db.session.commit()
        return render_template('index.html', users=db_users)
    return redirect('auth_views/signin.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    ''' Sign's user in and renders login view'''

    # Create form instance
    form = LoginForm()

    if request.method == "POST":
        db_data = User.query.filter_by(email=form.email.data).first()
        if db_data == None:
            return render_template('auth_views/signin.html', form=form, msg="Account not found")
        if check_password_hash(db_data.password, form.password.data):
            session['logged_in'] = True
            session['username'] = db_data.username

            return render_template('protected_views/home.html')
    return render_template('auth_views/signin.html', form=form)

    '''
    form = LoginForm()

    input_username = ''
    input_password = ''

    if form.validate_on_submit():
        input_email = form.email.data
        input_password = form.password.data

        # Get database details
        db_data = User.query.filter_by(email=input_email).first()

        if db_data == None:
            return render_template('auth_views/signin.html', form=form, msg="Account does not exist")
        # Validate data for login
        if check_password_hash(db_data.password, input_password):
            user_name = db_data.username
            return render_template('protected_views/home.html', user=user_name)

    return render_template('auth_views/signin.html', form=form)
    '''


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    msg = None
    try:
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = generate_password_hash(form.password.data)

            # Add user to db
            db.create_all()
            db.session.add(User(username, email, password))
            db.session.commit()

            return redirect('/signin')
        else:
            return render_template('auth_views/signup.html', form=form)
    except Exception as e:
        error = None
        return render_template('auth_views/signup.html', error=e.message, form=form)
