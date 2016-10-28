from flask import Flask
from flask_socketio import SocketIO
from flask_admin import Admin
from gm import GameManager
from config import *
from flask_wtf.csrf import CsrfProtect
from db import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = secret
app.config['SQLALCHEMY_DATABASE_URI']=DB_ADDRESS
app.config['PRESERVE_CONTEXT_ON_EXCEPTION']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)
socketio = SocketIO(app,engineio_logger=False,ping_timeout=30)
admin = Admin(app, name='A2050', template_mode='bootstrap3')
CsrfProtect(app)

gm=GameManager()

import admin
import pages
import socketioutils


with app.app_context():
    db.create_all()
    if db.session.query(User).count() == 0:
        user = User(nick='blue', password='blue', group=3)
        db.session.add(user)
        db.session.commit()
