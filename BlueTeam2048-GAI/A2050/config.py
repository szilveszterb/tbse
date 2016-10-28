import os
from flask import session

DIR_UP = (0, -1)
DIR_DOWN = (0, 1)
DIR_RIGHT = (1, 0)
DIR_LEFT = (-1, 0)

keymap={37:DIR_LEFT,38:DIR_UP,39:DIR_RIGHT,40:DIR_DOWN,87:DIR_UP,83:DIR_DOWN,65:DIR_LEFT,68:DIR_RIGHT}

treshold=5
secret=os.urandom(32)
DB_ADDRESS="mysql+pymysql://root:root@db/tbse"

def isLoggedIn():
    if "uid" in list(session.keys()):
        from db import User
        u = User.query.get(session["uid"])
        if u!= None:
            return True
    return False

def isGuest():
    if "uid" in list(session.keys()):
        from db import User
        u = User.query.get(session["uid"])
        if u.group<=1:
            return True
    return False

def isAdmin():
    if "uid" in list(session.keys()):
        from db import User
        u = User.query.get(session["uid"])
        if u.group==3:
            return True
    return False
