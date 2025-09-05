"""Celery tasks for dog operations."""

import asyncio
import time
from typing import Dict, Any

from app.tasks.celery_app import celery_app
from app.services.external_api import get_random_dog_image
from app.config.database import init_db, close_db
from app.models.dog import Dog


@celery_app.task
def create_dog_async(name: str, is_adopted: bool, id_user: int = None) -> Dict[str, Any]:
    """Asynchronous task to create a dog with external API call."""
    
    async def _create_dog():
        # Initialize database connection
        await init_db()
        
        try:
            # Simulate some latency as mentioned in requirements
            time.sleep(2)
            
            # Get random dog image from external API
            picture_url = await get_random_dog_image()
            
            if picture_url is None:
                picture_url = "https://images.dog.ceo/breeds/hound-afghan/n02088094_1007.jpg"
            
            # Create dog in database
            dog = await Dog.create(
                name=name,
                picture=picture_url,
                is_adopted=is_adopted,
                id_user_id=id_user if id_user else None
            )
            
            return {
                "id": dog.id,
                "name": dog.name,
                "picture": dog.picture,
                "create_date": dog.create_date.isoformat(),
                "is_adopted": dog.is_adopted,
                "id_user": dog.id_user_id
            }
        
        finally:
            # Close database connection
            await close_db()
    
    # Run the async function
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(_create_dog())
        return result
    finally:
        loop.close()


@celery_app.task
def get_worker_status() -> Dict[str, str]:
    """Task to check if worker is functioning."""
    time.sleep(1)  # Simulate some work
    return {"status": "Worker is functioning correctly", "timestamp": time.time()}