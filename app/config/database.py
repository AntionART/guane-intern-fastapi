"""Database configuration using Tortoise ORM."""

from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from app.config.settings import settings

TORTOISE_ORM = {
    "connections": {"default": settings.database_url},
    "apps": {
        "models": {
            "models": ["app.models.dog", "app.models.user", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def init_db():
    """Initialize database connection."""
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()


async def close_db():
    """Close database connection."""
    await Tortoise.close_connections()


def register_db(app):
    """Register database with FastAPI app."""
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )