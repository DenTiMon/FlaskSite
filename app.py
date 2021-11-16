from flask import Flask, render_template, request, flash, redirect, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user
import config
from db.users_control import FDataBase
import psycopg2
from config import HOST, DB_USER, DB_PASSWORD, DB_NAME
from db.UserLogin import UserLogin

app = Flask(__name__)
dbase = None
app.config['SECRET_KEY'] = config.SECRET_KEY

login_manager = LoginManager(app)
menu = ['Главная страница', 'Создать проект', 'Авторизация']


@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().fromDB(user_id, dbase)


# Подключение к БД
def connect_db():
    try:
        connection = psycopg2.connect(
            host=HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME)

        # connection.autocommit = True
        return connection

    except Exception as _ex:
        print('[INFO] Error while working with PostgreSQL', _ex)


# Создание БД
def create_db():
    db = connect_db()
    with app.open_resource('db/sq_db.db', mode='r') as f:
        db.cursor().execute(f.read())
        db.commit()
        db.close()


# Соединение с БД, если оно не установлено
def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


# Установление соединения с БД перед выполнением запроса
@app.before_request
def before_request():
    global dbase
    db = connect_db()
    dbase = FDataBase(db)


# Закрытие соединения, если оно было установлено
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


# Регистрация и авторизация пользователя
@app.route('/auth', methods=['POST', 'GET'])
def auth_reg():
    if request.method == 'POST':
        # Авторизация
        if request.form['btn'] == 'login':
            user = dbase.getUserByEmail(request.form['email_login'])
            if user and check_password_hash(user[3], request.form['password_login']):
                userlogin = UserLogin().create(user)
                login_user(userlogin)
                return redirect(url_for('index'))
            flash('Неверная пара логин/пароль', 'error')
        # Регистрация
        if request.form['btn'] == 'register':
            if 4 <= len(request.form['login_reg']) <= 20 and len(request.form['password_reg']) > 4 and \
                    request.form['password_reg'] == request.form['password2_reg']:
                hash = generate_password_hash(request.form['password_reg'])
                res = dbase.add_user(request.form['email_reg'], request.form['login_reg'], hash)
                if res:
                    flash('Вы успешно зарегистрировались', 'success')
                    return redirect('/new')
                else:
                    flash('Ошибка при добавлении в БД', 'error')
            else:
                if len(request.form['login_reg']) <= 4:
                    flash('Длина логина должна быть больше 4 симоволов', 'error')
                    print('Длина логина должна быть больше 4 симоволов', 'error')
                elif len(request.form['login_reg']) >= 20:
                    flash('Длина логина должна быть меньше 20 симоволов', 'error')
                    print('Длина логина должна быть меньше 20 симоволов', 'error')
                elif len(request.form['password_reg']) < 4:
                    flash('Длина пароля должна быть больше 4 симоволов', 'error')
                    print('Длина пароля должна быть больше 4 симоволов', 'error')
                elif request.form['password_reg'] != request.form['password2_reg']:
                    flash('Пароли не совпадают', 'error')
                    print('Пароли не совпадают', 'error')

    return render_template('auth.html', title='Форма авторизации и регистрации')


@app.route('/')
def index():
    return render_template('index.html', menu=menu)


@app.route('/new')
def new():
    print(url_for('new'))
    return render_template('new.html')


if __name__ == '__main__':
    app.run(debug=True)
