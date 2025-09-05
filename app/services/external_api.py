"""External API service for fetching dog images."""

import httpx
from typing import Optional

from app.config.settings import settings


async def get_random_dog_image() -> Optional[str]:
    """Fetch a random dog image from dog.ceo API."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(settings.dog_ceo_api_url)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "success":
                return data.get("message")
            return None
    except Exception as e:
        print(f"Error fetching dog image: {e}")
        return None