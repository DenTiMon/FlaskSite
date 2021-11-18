from flask import Blueprint, render_template, current_app, request, redirect, url_for, flash
from flask_login import login_user, LoginManager
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.authmodule.models import User

auth = Blueprint('auth', __name__)


@auth.route('/auth', methods=['POST', 'GET'])
def auth_reg():
    if request.method == 'POST':
        # Авторизация
        if request.form.get('btn') == 'login':
            email_login = request.form.get('email_login')
            password_login = request.form.get('password_login')

            user = User.query.filter_by(email=email_login).first()
            if not user or not check_password_hash(user.password, password_login):
                flash('Неверное имя пользователя или пароль')
                return 'Неверное имя пользователя или пароль'
            login_user(user)
            return 'Вы успешно вошли'

        # Регистрация
        if request.form.get('btn') == 'register':
            email_reg = request.form.get('email_reg')
            login_reg = request.form.get('login_reg')
            password_reg = request.form.get('password_reg')
            password2_reg = request.form.get('password2_reg')

            user = User.query.filter_by(email=email_reg).first()

            if user:
                flash('Email address already exists')
                return 'Пользователь уже существует'
            if password_reg != password2_reg:
                flash('Password')
                return 'Пароли не совпадают'
            if len(password_reg) < 4:
                flash('Password')
                return 'Слишком короткий пароль'
            if len(login_reg) < 4:
                flash('Login')
                return 'Слишком короткий логин'

            new_user = User(email=email_reg, login=login_reg, password=generate_password_hash(password_reg))

            db.session.add(new_user)
            db.session.commit()
            return 'Регистрация прошла успешно'

    return render_template('authmodule/auth.html', title='Форма авторизации и регистрации')




