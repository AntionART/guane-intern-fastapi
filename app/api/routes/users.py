"""User routes with basic CRUD operations."""

from typing import List
from fastapi import APIRouter, HTTPException, status
from tortoise.exceptions import DoesNotExist, IntegrityError

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserWithDogs

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def get_users():
    """Get all users."""
    users = await User.all()
    return [UserResponse.from_orm(user) for user in users]


@router.get("/{user_id}", response_model=UserWithDogs)
async def get_user_by_id(user_id: int):
    """Get user by ID with their dogs."""
    try:
        user = await User.get(id=user_id).prefetch_related("dogs")
        return UserWithDogs.from_orm(user)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):
    """Create a new user."""
    try:
        user = await User.create(
            name=user_data.name,
            last_name=user_data.last_name,
            email=user_data.email
        )
        return UserResponse.from_orm(user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email '{user_data.email}' already exists"
        )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserUpdate):
    """Update user by ID."""
    try:
        user = await User.get(id=user_id)
        update_data = user_data.dict(exclude_unset=True)
        
        if update_data:
            await user.update_from_dict(update_data)
            await user.save()
        
        return UserResponse.from_orm(user)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )


@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    """Delete user by ID."""
    try:
        user = await User.get(id=user_id)
        await user.delete()
        return {"message": f"User with id {user_id} deleted successfully"}
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )