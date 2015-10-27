import os

from pymongo import Connection

from flask import Flask
from flask.ext.pymongo import PyMongo
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID

from config import basedir
from app import views


collection = Connection()["test-site"]

app = Flask(__name__)
app.config.from_object('config')
mongo = PyMongo(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))
