"""Authentication routes."""

from fastapi import APIRouter, HTTPException, status
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel

from app.core.auth import create_token_for_user, Token

router = APIRouter()


class LoginRequest(BaseModel):
    """Login request schema."""
    username: str
    password: str


@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    """Login endpoint to get access token."""
    # Simple authentication - in production, verify against database
    if login_data.username == "admin" and login_data.password == "secret":
        token_data = create_token_for_user(login_data.username)
        return Token(**token_data)
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )