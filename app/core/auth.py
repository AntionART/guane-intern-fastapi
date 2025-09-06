"""Authentication core functionality."""

from datetime import datetime, timedelta
from typing import Any, Optional

from jose import JWTError, jwt
from pydantic import BaseModel

from app.config.settings import settings


class TokenData(BaseModel):
    """Token data schema."""
    username: Optional[str] = None


class Token(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str


def decode_access_token(token: str) -> Optional[str]:
    """Decode access token and return username."""
    try:
        payload = jwt.decode(
            token, 
            settings.secret_key, 
            algorithms=[settings.algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None


def create_token_for_user(username: str) -> dict:
    """Create token for user."""
    from app.core.security import create_access_token
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        subject=username, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    } 