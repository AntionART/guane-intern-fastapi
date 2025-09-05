"""User schemas for request/response validation."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user schema."""
    name: str
    last_name: str
    email: EmailStr


class UserCreate(UserBase):
    """User creation schema."""
    pass


class UserUpdate(BaseModel):
    """User update schema."""
    name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    """User response schema."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic config."""
        from_attributes = True


class UserWithDogs(UserResponse):
    """User response schema with dogs."""
    dogs: List["DogResponse"] = []
    
    class Config:
        """Pydantic config."""  
        from_attributes = True


# Import here to avoid circular imports
from app.schemas.dog import DogResponse
UserWithDogs.model_rebuild()