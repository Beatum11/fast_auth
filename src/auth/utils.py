from passlib.context import CryptContext
import jwt
from src.config import settings
from datetime import datetime, timedelta, timezone
import uuid


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def create_jwt_token(user_data: dict,
                     expires_delta: timedelta,
                     token_type: str = 'access'):
    now = datetime.now(timezone.utc)
    expire = now + expires_delta

    secret = settings.JWT_SECRET

    payload: dict = {
        "user": user_data,
        "exp": expire,
        "iat": now,
        "jti": str(uuid.uuid4()),
        "type": token_type
    }

    return jwt.encode(payload, secret, settings.JWT_ALGO)


def create_refresh_token(user_data: dict):
    expires_delta = timedelta(days=30)

    return create_jwt_token(
        user_data,
        expires_delta,
        token_type='refresh'
    )


def create_access_token(user_data: dict):
    expires_delta = timedelta(minutes=15)

    return create_jwt_token(
        user_data,
        expires_delta
    )


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGO])
        
        