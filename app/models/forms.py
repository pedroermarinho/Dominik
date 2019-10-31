from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired , Email

# csrf = CSRFProtect()


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired('não pode ficar vazio')])
    password = PasswordField("password", validators=[DataRequired('não pode ficar vazio')])
    remember = BooleanField("remember")


class RegisterForm(FlaskForm):
    name = StringField("name", validators=[DataRequired('não pode ficar vazio')])
    username = StringField("username", validators=[DataRequired('não pode ficar vazio')])
    email = StringField("email", validators=[DataRequired('não pode ficar vazio'),Email()])
    password = PasswordField("password", validators=[DataRequired('não pode ficar vazio')])


