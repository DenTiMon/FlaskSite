from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.HOST}/{Config.DB_NAME}'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from app.authmodule.models import User

    @login_manager.user_loader
    def load_user(user_id):
        print('load_user')
        return User.query.get(int(user_id))

    import app.authmodule.controllers as authmodule

    app.register_blueprint(authmodule.auth)

    return app
