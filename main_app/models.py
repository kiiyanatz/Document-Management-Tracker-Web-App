from flask import Flask
from main_app import db


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(100))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


class Document(db.Model):

    '''
    Model for the documents
    '''
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    link = db.Column(db.String(255), unique=True)
    keywords = db.Column(db.String(255))
    department = db.Column(db.String(80))
    file_path = db.Column(db.String(100))
    uploader = db.Column(db.String(100))

    def __init__(self, title, link, keywords, department, file_path, uploader):
        self.title = title
        self.link = link
        self.keywords = keywords
        self.department = department
        self.file_path = file_path
        self.uploader = uploader
