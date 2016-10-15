from flask import render_template,request,session,redirect,url_for
from db import User,getSessionScores,Session
from forms import LoginForm,SessionForm
from app import app,db
from config import isLoggedIn,isGuest,isAdmin

@app.route('/',methods=("GET","POST"))
def login():
    if "uid" in list(session.keys()):
        return redirect(url_for("_choose"))
    form=LoginForm(request.form)
    if form.validate_on_submit():
        user=User.query.filter_by(nick=form.nick.data).first()
        if user!= None:
            if user.password==form.password.data:
                session["uid"]=user.id
                if user.group==3:
                    return redirect(url_for("_choose"))
                else:
                    return redirect(url_for("index"))
        else:
            return "Auth problem"
    return render_template("login.html",form=form)

@app.route('/game/')
def index():
    if isLoggedIn():
        scores=getSessionScores()
        if isGuest():
            return render_template("index.html",guest=True,scores=scores)
        else:
            return render_template("index.html",guest=False,scores=scores)
    else:
        return redirect(url_for("login"))

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route('/choose/')
def _choose():
    if isLoggedIn() and isAdmin():
        u=User.query.get(session["uid"])
        return render_template("choose.html",user=u)
    else:
        return redirect(url_for("login"))

@app.route("/session/",methods=("GET","POST"))
def _session():
    if isLoggedIn() and isAdmin():
        u=User.query.get(session["uid"])
        form=SessionForm(request.form)
        if form.validate_on_submit():
            s=Session(form.count.data)
            db.session.add(s)
            db.session.commit()
        return render_template("session.html",scores=getSessionScores(),user=u,form=form)
    else:
        return redirect(url_for("login"))
