from datetime import datetime
from enum import Enum

from flask_login import UserMixin
from sqlalchemy import UniqueConstraint

from database import db


class Role(str, Enum):
    STUDENT = "student"
    COOK = "cook"
    ADMIN = "admin"


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(16), nullable=False, default=Role.STUDENT.value)

    # Для ученика
    allergies = db.Column(db.Text, nullable=True)
    preferences = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("username", name="uq_users_username"),
        UniqueConstraint("email", name="uq_users_email"),
    )

    def is_admin(self) -> bool:
        return self.role == Role.ADMIN.value

    def is_cook(self) -> bool:
        return self.role == Role.COOK.value

    def is_student(self) -> bool:
        return self.role == Role.STUDENT.value
