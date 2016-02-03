from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension


# Create flask application
app = Flask(__name__, instance_relative_config=True)

bootstrap = Bootstrap(app)

# Load config file
app.config.from_object('config')	

# Database base model
db = SQLAlchemy(app)

toolbar = DebugToolbarExtension(app)

import main_app.views
