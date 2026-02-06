from datetime import datetime

from database import db


class ProcurementRequest(db.Model):
    __tablename__ = "procurement_requests"

    id = db.Column(db.Integer, primary_key=True)
    created_by_cook_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    status = db.Column(db.String(16), nullable=False, default="pending")  # pending/approved/rejected
    comment = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    decided_at = db.Column(db.DateTime, nullable=True)

    created_by = db.relationship("User", backref="procurement_requests")

    items = db.relationship("ProcurementItem", backref="request", cascade="all, delete-orphan")


class ProcurementItem(db.Model):
    __tablename__ = "procurement_items"

    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey("procurement_requests.id"), nullable=False)

    product_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=0.0)
    unit = db.Column(db.String(16), nullable=False, default="kg")
