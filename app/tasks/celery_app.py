"""Celery application configuration."""

import os
from celery import Celery

from app.config.settings import settings

# Create Celery instance
celery_app = Celery(
    "guane_dogs",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.tasks.dog_tasks"]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    result_expires=3600,
)

