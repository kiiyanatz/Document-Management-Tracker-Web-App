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
    document_name = db.Column(db.String(80), unique=True)
    document_keywords = db.Column(db.String(255))

class Department(db.Model):
    '''
    The database model for each department
    '''
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    dep_name = db.Column(db.String(80), unique=True)
