"""Dog schemas for request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DogBase(BaseModel):
    """Base dog schema."""
    name: str
    is_adopted: bool = False
    id_user: Optional[int] = None


class DogCreate(BaseModel):
    """Dog creation schema."""
    name: str
    is_adopted: bool = False
    id_user: Optional[int] = None


class DogUpdate(BaseModel):
    """Dog update schema."""
    name: Optional[str] = None
    picture: Optional[str] = None
    is_adopted: Optional[bool] = None
    id_user: Optional[int] = None


class DogResponse(DogBase):
    """Dog response schema."""
    id: int
    picture: str
    create_date: datetime
    
    class Config:
        """Pydantic config."""
        from_attributes = True


class DogWithUser(DogResponse):
    """Dog response schema with user information."""
    user: Optional["UserResponse"] = None
    
    class Config:
        """Pydantic config."""
        from_attributes = True


# Import here to avoid circular imports
from app.schemas.user import UserResponse
DogWithUser.model_rebuild()