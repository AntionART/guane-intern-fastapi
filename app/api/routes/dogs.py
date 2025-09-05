"""Dog routes following REST principles."""

from typing import List
from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks

from app.api.dependencies import get_current_user
from app.schemas.dog import DogCreate, DogUpdate, DogResponse
from app.services.dog_service import DogService
from app.tasks.dog_tasks import create_dog_async

router = APIRouter()


@router.get("/", response_model=List[DogResponse])
async def get_dogs():
    """Get all dogs."""
    return await DogService.get_all_dogs()


@router.get("/is_adopted", response_model=List[DogResponse])
async def get_adopted_dogs():
    """Get all adopted dogs."""
    return await DogService.get_adopted_dogs()


@router.get("/{name}", response_model=DogResponse)
async def get_dog_by_name(name: str):
    """Get dog by name."""
    dog = await DogService.get_dog_by_name(name)
    if not dog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dog with name '{name}' not found"
        )
    return dog


@router.post("/{name}", response_model=dict)
async def create_dog(
    name: str,
    dog_data: DogCreate,
    current_user: str = Depends(get_current_user)
):
    """Create a new dog (protected route with JWT)."""
    # Override name from path parameter
    dog_data.name = name
    
    # Check if dog already exists
    existing_dog = await DogService.get_dog_by_name(name)
    if existing_dog:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Dog with name '{name}' already exists"
        )
    
    # Start async task
    task = create_dog_async.delay(
        name=dog_data.name,
        is_adopted=dog_data.is_adopted,
        id_user=dog_data.id_user
    )
    
    return {
        "message": f"Dog '{name}' creation started",
        "task_id": task.id,
        "status": "processing"
    }


@router.put("/{name}", response_model=DogResponse)
async def update_dog(name: str, dog_data: DogUpdate):
    """Update dog by name."""
    try:
        dog = await DogService.update_dog(name, dog_data)
        if not dog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dog with name '{name}' not found"
            )
        return dog
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{name}", response_model=dict)
async def delete_dog(name: str):
    """Delete dog by name."""
    deleted = await DogService.delete_dog(name)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dog with name '{name}' not found"
        )
    return {"message": f"Dog '{name}' deleted successfully"}