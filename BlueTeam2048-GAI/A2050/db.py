import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(32),default="Unnamed player",nullable=False)
    password=db.Column(db.String(32),nullable=False)
    group = db.Column(db.Integer, default=0)
    points= db.Column(db.Integer, default=0)

    def __init__(self,nick="Unnamed player",password="pass",group=0):
        self.nick=nick
        self.password=password
        self.group=group
        self.points=0

    def __repr__(self):
        return self.nick


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime,default=datetime.datetime.utcnow,nullable=False)
    games = db.Column(db.Integer,nullable=False,default=5)

    def __init__(self,games):
        self.games=games

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship('User')
    hightile = db.Column(db.Integer, default=2)
    points = db.Column(db.Integer,default=0)
    start = db.Column(db.DateTime,default=datetime.datetime.utcnow)

    def __init__(self, user):
        self.user=user


def calcScore(game):
    return game.points+10*game.hightile

def getSessionScores():
    s=Session.query.order_by(db.desc(Session.start)).first()
    if s != None:
        date=s.start
        g=Game.query.filter(Game.start>date).all()
        users=User.query.all()
        scores=dict()
        for u in users:
            if u.group==0:
                continue
            sc=0
            gc=0
            for game in g:
                if gc>=s.games:
                    break;
                if game.user==u:
                    sc+=calcScore(game)
                    gc+=1
            if gc!=0:
                scores[u.nick]=(sc,min(gc,s.games))

        return scores
    return None
