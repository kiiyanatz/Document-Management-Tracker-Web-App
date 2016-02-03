from main_app import app
from flask import Flask, render_template, request, session, redirect
from .forms import LoginForm
from .forms import SignUpForm
from main_app import db
from main_app.models import User
from werkzeug.security import check_password_hash, generate_password_hash

@app.route('/')
def home():
    db_users = User.query.all()
    db.session.commit()
    return render_template('index.html', users=db_users)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    ''' Sign's user in and renders login view'''

    # Create form instance
    form = LoginForm()
    msg = ''

    if request.method == "POST":
        db_data = User.query.filter_by(email=form.email.data).first()

        if db_data == None:
            return render_template('auth_views/signin.html', form=form, msg='Account not found')
        elif check_password_hash(db_data.password, form.password.data):
            session['logged_in'] = True
            session['username'] = db_data.username
            return redirect('/protected_views/home.html')
        else:
            return render_template('auth_views/signin.html', form=form, msg="Wrong password or email")
    else:
        return render_template('auth_views/signin.html', form=form)

@app.route('/protected_views/home.html', methods=['GET', 'POST'])
def user_home():
    if session.get('username') == None:
        return redirect('/signin')
    else:
        return render_template('protected_views/home.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


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
