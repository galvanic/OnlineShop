from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

###

app = Flask(__name__)

app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

###

import webapp.routes