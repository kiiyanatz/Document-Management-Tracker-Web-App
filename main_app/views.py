from flask import Flask, render_template, request, session, redirect, flash, json, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug import secure_filename
from sqlalchemy import text
import os

from .forms import LoginForm, SignUpForm, FileUploadForm, SearchForm
from .models import db, User, Document, Department
from main_app import app


@app.route('/')
def home():
    if session.get('username') is None:
        return render_template('index.html')
    else:
        return render_template('index.html', dashboard=True)


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
    top_documents = Document.query.order_by(Document.id.desc()).limit(5).all()
    # Pagination
    page = request.args.get('page', 1, type=int)
    pagination = Document.query.order_by(Document.id.desc()).paginate(
        page, per_page=10,
        error_out=False)
    documents = pagination.items
    if request.method == "POST":
        # try:
        if form.validate_on_submit():
            title = form.title.data
            link = form.link.data
            keyword = form.keywords.data
            dep = form.department.data

            filedata = form.file_path.data
            newfilename = secure_filename(filedata.filename)
            uploader = session['username']

            # Save to file system
            form.file_path.data.save('./main_app/static/uploads/' + newfilename)

            # File abspath
            #basedir = os.path.abspath(os.path.dirname(__file__))
            file_path = url_for('static', filename='uploads/'+newfilename)

            # Add document to db
            db.session.add(
                Document(title, link, keyword, dep, file_path, uploader))
            db.session.commit()

            return redirect('/protected_views/home.html')
        else:
            return render_template('protected_views/home.html',
                                   form=form,
                                   search_form=search_form,
                                   titles=titles,
                                   username=session['username'],
                                   top_documents=top_documents,
                                   pagination=pagination,
                                   posts=documents,
                                   docus=docus)

    return render_template('protected_views/home.html',
                           form=form,
                           search_form=search_form,
                           titles=titles,
                           username=session['username'],
                           top_documents=top_documents,
                           pagination=pagination,
                           posts=documents,
                           docus=docus)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/download/<filename>')
def download(filename):
    pass


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = generate_password_hash(form.password.data)

        # Add user to db
        db.session.add(User(username, email, password))
        db.session.commit()

        return redirect('/signin')
    else:
        return render_template('auth_views/signup.html', form=form)
