from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap



# Create flask application
app = Flask(__name__, instance_relative_config=True)

bootstrap = Bootstrap(app)

# Load config file
app.config.from_object('config')	

# Database base model
db = SQLAlchemy(app)



import main_app.views
