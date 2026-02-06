from datetime import datetime

from database import db


class ProductStock(db.Model):
    __tablename__ = "product_stocks"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False, unique=True)
    quantity = db.Column(db.Float, nullable=False, default=0.0)
    unit = db.Column(db.String(16), nullable=False, default="kg")

    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class DishStock(db.Model):
    __tablename__ = "dish_stocks"

    id = db.Column(db.Integer, primary_key=True)

    dish_name = db.Column(db.String(120), nullable=False, unique=True)
    portions_available = db.Column(db.Integer, nullable=False, default=0)

    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
