from app import admin,db
from flask_admin.contrib.sqla import ModelView
from db import User,Game
from config import isLoggedIn
from flask import redirect,url_for

class RestrictedModelView(ModelView):

    def is_accessible(self):
        return isLoggedIn()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login"))

admin.add_view(RestrictedModelView(User,db.session))
admin.add_view(RestrictedModelView(Game,db.session))
