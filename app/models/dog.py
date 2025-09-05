"""Dog model."""

from tortoise import fields
from tortoise.models import Model


class Dog(Model):
    """Dog model for storing dog information."""
    
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True)
    picture = fields.TextField()
    create_date = fields.DatetimeField(auto_now_add=True)
    is_adopted = fields.BooleanField(default=False)
    id_user = fields.ForeignKeyField(
        "models.User", 
        related_name="dogs", 
        null=True, 
        on_delete=fields.SET_NULL
    )
    
    class Meta:
        """Meta configuration for Dog model."""
        table = "dogs"
    
    def __str__(self) -> str:
        """String representation of Dog."""
        return f"{self.name} (Adopted: {self.is_adopted})"