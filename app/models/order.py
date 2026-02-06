from datetime import datetime, date

from database import db


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # "single" / "subscription"
    payment_type = db.Column(db.String(16), nullable=False)

    amount_rub = db.Column(db.Integer, nullable=False)

    # статус
    status = db.Column(db.String(16), nullable=False, default="paid")  # demo: always paid

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    student = db.relationship("User", backref="payments")


class MealOrder(db.Model):
    __tablename__ = "meal_orders"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    day = db.Column(db.Date, nullable=False, default=date.today)
    meal_type = db.Column(db.String(16), nullable=False)  # breakfast/lunch

    paid = db.Column(db.Boolean, default=False, nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey("payments.id"), nullable=True)

    # отметка получения
    received_by_student_at = db.Column(db.DateTime, nullable=True)
    issued_by_cook_at = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    student = db.relationship("User", backref="meal_orders")
    payment = db.relationship("Payment", backref="meal_orders")

    __table_args__ = (
        db.UniqueConstraint("student_id", "day", "meal_type", name="uq_student_day_meal"),
    )
