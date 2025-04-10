from django.db import models
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

class Family(models.Model):
    family_name = models.CharField(max_length=100)
    invite_code = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_invite_url(self):
        return f"http://127.0.0.1:8000/families/join/{self.invite_code}/"
    
    def __str__(self):
        return self.family_name