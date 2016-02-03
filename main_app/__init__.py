from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager


# Create flask application
app = Flask(__name__, instance_relative_config=True)

bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Set the login view
login_manager.login_view = 'auth_views/signin.html'

# Load config file
app.config.from_object('config')

# Database base model
db = SQLAlchemy(app)

import main_app.views
