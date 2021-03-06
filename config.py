import os

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = "slkdjf49859043kdjg43398"

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

UPLOAD_FOLDER = basedir + '/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'docx', 'doc'])

DEBUG_TB_PROFILER_ENABLED = True
