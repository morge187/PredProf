import os
from datetime import timedelta


class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///canteen.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REMEMBER_COOKIE_DURATION = timedelta(days=14)
    WTF_CSRF_TIME_LIMIT = None

    # Демо-настройка: "платежи" помечаем как успешные в приложении
    PAYMENT_DEMO_MODE = True
