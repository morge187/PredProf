from sqlalchemy import (
    Column, String, Integer, Boolean, DateTime, UUID,
    ForeignKey, JSON, Numeric
)
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4
from database import Base


class User(Base):
    __tablename__ = "users"

    # Данные для входа
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String(254), unique=True, nullable=False, index=True)
    passwordHash = Column(String(255), nullable=False)

    # роль
    role = Column(String(20), default="STUDENT", nullable=False)
    isActive = Column(Boolean, default=True, nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # связи
    student_profile = relationship("StudentProfile", back_populates="user", uselist=False)
    cook_profile = relationship("CookProfile", back_populates="user", uselist=False)
    payments = relationship("Payment", back_populates="user")
    meal_marks = relationship("MealMark", back_populates="user")
    reviews = relationship("Review", back_populates="user")


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    class_name = Column(String(50), nullable=True)
    allergies = Column(JSON, nullable=True)
    preferences = Column(JSON, nullable=True)

    user = relationship("User", back_populates="student_profile")


class CookProfile(Base):
    __tablename__ = "cook_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    position = Column(String(100), nullable=True)

    user = relationship("User", back_populates="cook_profile")


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    dish_type = Column(String(20), nullable=False)   # Блюдо на завтрак или обед
    price = Column(Numeric(10, 2), nullable=False)
    calories = Column(Integer, nullable=True)
    allergens = Column(JSON, nullable=True)          # список аллергенов

    menu_items = relationship("MenuItem", back_populates="dish")
    reviews = relationship("Review", back_populates="dish")


class Menu(Base):
    __tablename__ = "menus"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    date = Column(DateTime, nullable=False, index=True)
    meal_type = Column(String(20), nullable=False)   # завтрак или обед

    items = relationship("MenuItem", back_populates="menu")


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    menu_id = Column(UUID(as_uuid=True), ForeignKey("menus.id"), nullable=False)
    dish_id = Column(UUID(as_uuid=True), ForeignKey("dishes.id"), nullable=False)
    planned_quantity = Column(Integer, nullable=True)   # сколько планируется приготовить

    menu = relationship("Menu", back_populates="items")
    dish = relationship("Dish", back_populates="menu_items")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow, nullable=False)

    amount = Column(Numeric(10, 2), nullable=False)
    payment_type = Column(String(20), nullable=False)  # одиночный или по абонименту
    status = Column(String(20), nullable=False, default="PAID")  # оплачена или отменено

    # привязка к конкретному приёму пищи или абонементу
    menu_id = Column(UUID(as_uuid=True), ForeignKey("menus.id"), nullable=True)
    subscription_from = Column(DateTime, nullable=True)
    subscription_to = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="payments")
    menu = relationship("Menu")


class MealMark(Base):
    __tablename__ = "meal_marks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    menu_id = Column(UUID(as_uuid=True), ForeignKey("menus.id"), nullable=False)

    marked_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # чтобы не было повторной отметки на тот же приём пищи

    user = relationship("User", back_populates="meal_marks")
    menu = relationship("Menu")


class ServedDish(Base):
    __tablename__ = "served_dishes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    menu_item_id = Column(UUID(as_uuid=True), ForeignKey("menu_items.id"), nullable=False)
    served_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    menu_item = relationship("MenuItem")


class StockItem(Base):
    __tablename__ = "stock_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(200), nullable=False)          # продукт: картофель, молоко
    unit = Column(String(20), nullable=False)           # кг, л, шт
    quantity = Column(Numeric(10, 2), nullable=False)   # текущий остаток
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PurchaseRequest(Base):
    __tablename__ = "purchase_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow, nullable=False)

    status = Column(String(20), default="PENDING", nullable=False)  # PENDING / APPROVED / REJECTED
    approved_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    approvedAt = Column(DateTime, nullable=True)

    items = relationship("PurchaseRequestItem", back_populates="request")
    created_by = relationship("User", foreign_keys=[created_by_id])
    approved_by = relationship("User", foreign_keys=[approved_by_id])


class PurchaseRequestItem(Base):
    __tablename__ = "purchase_request_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    request_id = Column(UUID(as_uuid=True), ForeignKey("purchase_requests.id"), nullable=False)

    product_name = Column(String(200), nullable=False)
    unit = Column(String(20), nullable=False)
    quantity = Column(Numeric(10, 2), nullable=False)

    request = relationship("PurchaseRequest", back_populates="items")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    dish_id = Column(UUID(as_uuid=True), ForeignKey("dishes.id"), nullable=False)

    rating = Column(Integer, nullable=False)   # 1–5
    comment = Column(String(1000), nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="reviews")
    dish = relationship("Dish", back_populates="reviews")