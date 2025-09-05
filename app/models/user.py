"""User model."""

from tortoise import fields
from tortoise.models import Model


class User(Model):
    """User model for storing user information."""
    
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    last_name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=255, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    class Meta:
        """Meta configuration for User model."""
        table = "users"
    
    def __str__(self) -> str:
        """String representation of User."""
        return f"{self.name} {self.last_name} ({self.email})"