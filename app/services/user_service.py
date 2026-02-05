import uuid
import logging
from datetime import datetime
from sqlalchemy.orm import Session

from models import User, StudentProfile
from auth import hash_password, verify_password
from utils.error import UserError

logger = logging.getLogger(__name__)


class UserService:
    @staticmethod
    def create_user(db: Session, user_data: dict) -> User:
        # Проверяем, что email уникален
        existing = db.query(User).filter(User.email == user_data["email"]).first()
        if existing:
            logger.warning(
                f"Attempt to create user with existing email: {user_data['email']}"
            )
            # Можно кидать свою ошибку или вернуть структуру под валидацию
            raise UserError(cause="Такой email уже существует", field="email")

        user = User(
            id=uuid.uuid4(),
            email=user_data["email"],
            passwordHash=hash_password(user_data["password"]),
            # role оставляем по умолчанию (STUDENT) из модели
            isActive=True,
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow(),
        )

        profile = StudentProfile(
            id=uuid.uuid4(),
            user_id=user.id,
            class_name=user_data.get("class_name"),  # имя поля подправь под свою схему
        )

        db.add(user)
        db.add(profile)
        db.commit()
        db.refresh(user)
        db.refresh(profile)

        logger.info(
            f"Created new user: {user.id} ({user.email}) with role {user.role}"
        )
        return user

    @staticmethod
    def get_user(db: Session, user_id: uuid.UUID):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise UserError(field="but", cause=f"Пользователь с таким id не найден")

        profile = (
            db.query(StudentProfile)
            .filter(StudentProfile.user_id == user_id)
            .first()
        )

        if not profile:
            return user, None
        return user, profile

    @staticmethod
    def list_users(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        role: str = "STUDENT",
    ):
        total = db.query(User).filter(User.role == role).count()

        users = (
            db.query(User)
            .filter(User.role == role)
            .order_by(User.createdAt)
            .offset(skip)
            .limit(limit)
            .all()
        )

        logger.info(f"Listed users: skip={skip}, limit={limit}, total={total}")
        return users, total

    @staticmethod
    def update_user(
        db: Session,
        user_id: uuid.UUID,
        update_data: dict,
        is_admin: bool = False,
    ) -> User:
        result = UserService.get_user(db, user_id)
        # get_user может вернуть строку с ошибкой
        if isinstance(result, str):
            return result
        user, profile = result

        # Обновление полей пользователя
        if "email" in update_data:
            user.email = update_data["email"]
        if "password" in update_data:
            user.passwordHash = hash_password(update_data["password"])

        # Админские поля
        if is_admin:
            if "role" in update_data:
                user.role = update_data["role"]
            if "isActive" in update_data:
                user.isActive = update_data["isActive"]

        # Обновление профиля ученика
        if profile:
            if "class_name" in update_data:
                profile.class_name = update_data["class_name"]

        user.updatedAt = datetime.utcnow()
        db.commit()
        db.refresh(user)

        logger.info(f"Updated user {user_id}: {list(update_data.keys())}")
        return user

    @staticmethod
    def deactivate_user(db: Session, user_id: uuid.UUID) -> User:
        result = UserService.get_user(db, user_id)
        if isinstance(result, str):
            return result
        user, _ = result

        user.isActive = False
        user.updatedAt = datetime.utcnow()
        db.commit()
        db.refresh(user)

        logger.info(f"Deactivated user {user_id} ({user.email})")
        return user

    @staticmethod
    def authenticate_user(
        db: Session,
        email: str,
        password: str,
    ) -> User:
        user = db.query(User).filter(User.email == email).first()

        if not user:
            logger.warning(f"Login attempt with non-existent email: {email}")
            raise UserError(cause="Пользователя не существует, надо зарегестрироваться", field="email")

        if not verify_password(password, user.passwordHash):
            logger.warning(f"Failed login attempt for user {user.id} ({email})")
            return UserError(cause="Неверный пароль", field="email")

        if not user.isActive:
            logger.warning(f"Login attempt for deactivated user {user.id} ({email})")
            return UserError(cause="пользователь заблокирован", field="email")

        logger.info(f"Successful login for user {user.id} ({email})")
        return user