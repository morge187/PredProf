from datetime import datetime, timedelta
import jwt
from settings import settings


def create_access_token(user_id: str, role: str) -> tuple:
    now = datetime.utcnow()
    expires = now + timedelta(hours=settings.JWT_EXPIRE_HOURS)
    
    payload = {
        "sub": user_id,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int(expires.timestamp()),
    }
    
    token = jwt.encode(
        payload,
        settings.RANDOM_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token, settings.JWT_EXPIRE_HOURS * 3600


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.RANDOM_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

decode_token = verify_token