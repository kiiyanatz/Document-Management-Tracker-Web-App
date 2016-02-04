from flask import Flask, render_template, request, session, redirect, flash, json
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug import secure_filename

from .forms import LoginForm, SignUpForm, FileUploadForm, SearchForm
from .models import db, User, Document, Department
from main_app import app
from sqlalchemy import text


@app.route('/')
def home():
    db.create_all()
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

        if db_data is None:
            return render_template('auth_views/signin.html',
                                   form=form, msg='Account not found')
        elif check_password_hash(db_data.password, form.password.data):
            session['logged_in'] = True
            session['username'] = db_data.username
            return redirect('/protected_views/home.html')
        else:
            return render_template('auth_views/signin.html',
                                   form=form, msg="Wrong password or email")
    else:
        return render_template('auth_views/signin.html', form=form)


@app.route('/protected_views/home.html', methods=['GET', 'POST'])
def user_home():
    if session.get('username') is None:
        flash("Login to continue")
        return redirect('/signin')

    form = FileUploadForm()
    search_form = SearchForm()
    docus = Document.query.all()
    titles = [form.title.name, form.keywords.name,
              form.department.name, form.uploader.name]
    if request.method == "POST":
        # try:
        if form.validate_on_submit():
            title = form.title.data
            link = form.link.data
            keyword = form.keywords.data
            dep = form.department.data

            filedata = form.file_path.data
            filename = secure_filename(filedata.filename)
            uploader = session['username']

            # Save to file system
            form.file_path.data.save('uploads/' + filename)

            # Add document to db
            db.session.add(
                Document(title, link, keyword, dep, 'upload/'+filename, uploader))
            db.session.commit()

            return redirect('/protected_views/home.html')
        else:
            return render_template('protected_views/home.html',
                                   form=form,
                                   search_form=search_form,
                                   titles=titles,
                                   username=session['username'],
                                   docus=docus)

    return render_template('protected_views/home.html',
                           form=form,
                           search_form=search_form,
                           titles=titles,
                           username=session['username'],
                           docus=docus)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if session.get('username') is None:
        flash("Login to continue")
        return redirect('/signin')

    form = FileUploadForm()
    search_form = SearchForm()
    docus = Document.query.all()
    titles = [form.title.name, form.keywords.name,
              form.department.name, form.uploader.name]

    search_q = request.args.get('q')
    search_field = request.args.get('search_category')

    result = db.engine.execute("select * from documents where :field = :term", {'field': search_field, 'term':search_q})
    return render_template('protected_views/home.html', docus=result, titles=titles, form=form)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form=SignUpForm()

    if form.validate_on_submit():
        username=form.username.data
        email=form.email.data
        password=generate_password_hash(form.password.data)

        # Add user to db
        db.create_all()
        db.session.add(User(username, email, password))
        db.session.commit()

        return redirect('/signin')
    else:
        return render_template('auth_views/signup.html', form=form)
