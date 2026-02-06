# app.py
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect

from settings import Settings
from database import db
from models import User
from routes import register_blueprints

login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Сначала загружаем конфиг, потом init_app расширений. [web:17][web:24]
    app.config.from_object(Settings)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Требуется авторизация."

    register_blueprints(app)

    with app.app_context():
        db.create_all()

    return app

@login_manager.user_loader
def load_user(user_id: str):
    try:
        return db.session.get(User, int(user_id))
    except Exception:
        return None
