from datetime import date, datetime

from database import db


class MenuDay(db.Model):
    __tablename__ = "menu_days"

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Date, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    items = db.relationship("MenuItem", backref="menu_day", cascade="all, delete-orphan")


class MenuItem(db.Model):
    __tablename__ = "menu_items"

    id = db.Column(db.Integer, primary_key=True)
    menu_day_id = db.Column(db.Integer, db.ForeignKey("menu_days.id"), nullable=False)

    # breakfast / lunch
    meal_type = db.Column(db.String(16), nullable=False)

    name = db.Column(db.String(120), nullable=False)
    price_rub = db.Column(db.Integer, nullable=False, default=0)

    # JSON-строка или обычный текст (простая версия)
    allergens = db.Column(db.String(255), nullable=True)

    is_active = db.Column(db.Boolean, default=True, nullable=False)
