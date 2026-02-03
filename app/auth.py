from functools import wraps
from flask import request
from passlib.context import CryptContext
from database import get_db_session
from models import User
# from utils.jwt_utils import verify_token
# from utils.errors import UnauthorizedError
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)