"""Dog service for business logic."""

from typing import List, Optional
from tortoise.exceptions import DoesNotExist

from app.models.dog import Dog
from app.models.user import User
from app.schemas.dog import DogCreate, DogUpdate, DogResponse
from app.services.external_api import get_random_dog_image


class DogService:
    """Service class for dog operations."""
    
    @staticmethod
    async def get_all_dogs() -> List[DogResponse]:
        """Get all dogs."""
        dogs = await Dog.all().prefetch_related("id_user")
        return [DogResponse.from_orm(dog) for dog in dogs]
    
    @staticmethod
    async def get_dog_by_name(name: str) -> Optional[DogResponse]:
        """Get dog by name."""
        try:
            dog = await Dog.get(name=name).prefetch_related("id_user")
            return DogResponse.from_orm(dog)
        except DoesNotExist:
            return None
    
    @staticmethod
    async def get_adopted_dogs() -> List[DogResponse]:
        """Get all adopted dogs."""
        dogs = await Dog.filter(is_adopted=True).prefetch_related("id_user")
        return [DogResponse.from_orm(dog) for dog in dogs]
    
    @staticmethod
    async def create_dog_sync(dog_data: DogCreate) -> DogResponse:
        """Create dog synchronously (for testing purposes)."""
        # Validate user exists if id_user is provided
        if dog_data.id_user:
            try:
                await User.get(id=dog_data.id_user)
            except DoesNotExist:
                raise ValueError(f"User with id {dog_data.id_user} does not exist")
        
        # Get random dog picture
        picture_url = await get_random_dog_image()
        if picture_url is None:
            picture_url = "https://images.dog.ceo/breeds/hound-afghan/n02088094_1007.jpg"
        
        # Create dog
        dog = await Dog.create(
            name=dog_data.name,
            picture=picture_url,
            is_adopted=dog_data.is_adopted,
            id_user_id=dog_data.id_user if dog_data.id_user else None
        )
        
        return DogResponse.from_orm(dog)
    
    @staticmethod
    async def update_dog(name: str, dog_data: DogUpdate) -> Optional[DogResponse]:
        """Update dog by name."""
        try:
            dog = await Dog.get(name=name)
            
            # Validate user exists if id_user is provided
            if dog_data.id_user:
                try:
                    await User.get(id=dog_data.id_user)
                except DoesNotExist:
                    raise ValueError(f"User with id {dog_data.id_user} does not exist")
            
            # Update fields
            update_data = dog_data.dict(exclude_unset=True)
            if "id_user" in update_data:
                update_data["id_user_id"] = update_data.pop("id_user")
            
            await dog.update_from_dict(update_data)
            await dog.save()
            
            return DogResponse.from_orm(dog)
        except DoesNotExist:
            return None
    
    @staticmethod
    async def delete_dog(name: str) -> bool:
        """Delete dog by name."""
        try:
            dog = await Dog.get(name=name)
            await dog.delete()
            return True
        except DoesNotExist:
            return False