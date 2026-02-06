from datetime import datetime

from database import db


class DishFeedback(db.Model):
    __tablename__ = "dish_feedback"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    dish_name = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1..5
    comment = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    student = db.relationship("User", backref="feedbacks")
