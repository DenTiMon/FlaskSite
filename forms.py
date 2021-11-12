from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[Email(), DataRequired()])
    login = StringField('Логин: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=4, max=20)])
    submit = SubmitField('Зарегистрироваться')