from sqlalchemy import Column, String, Integer, Boolean, DateTime, UUID, ForeignKey, JSON, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4
from database import Base

class User(Base):
    __tablename__ = "users"

    # Параметры пользователя
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String(254), unique=True, nullable=False, index=True)
    passwordHash = Column(String(255), nullable=False)

    # То что нужно будет программе
    role = Column(String(20), default="USER", nullable=False)
    isActive = Column(Boolean, default=True, nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)