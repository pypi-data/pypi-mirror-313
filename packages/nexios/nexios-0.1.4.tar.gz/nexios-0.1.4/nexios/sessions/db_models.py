from tortoise import fields
from tortoise.models import Model
class Session(Model):
    """Tortoise ORM model for storing session data."""
    id = fields.CharField(max_length=255, primary_key=True)
    data = fields.JSONField(default={})
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    def __str__(self):
        return f"Session {self.id}"