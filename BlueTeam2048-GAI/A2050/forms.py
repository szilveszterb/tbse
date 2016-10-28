from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired,NumberRange

class LoginForm(FlaskForm):
    nick = StringField("Nickname", validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Login", validators=[DataRequired()])

class SessionForm(FlaskForm):
    count = IntegerField("Turn count",validators=[DataRequired(),NumberRange(min=1)])
    submit = SubmitField("Start new session",validators=[DataRequired()])
