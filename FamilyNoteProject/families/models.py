from django.db import models
import uuid

class Family(models.Model):
    name = models.CharField(max_length=100)
    invite_code = models.UUIDField(default=uuid.uuid4, unique=True)
    
    def get_invite_url(self):
        return f"http://127.0.0.1:8000/families/join/{self.invite_code}/"
    
    def __str__(self):
        return self.name