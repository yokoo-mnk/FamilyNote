from django.db import models
import uuid

class Family(models.Model):
    name = models.CharField(max_length=100)
    invite_code = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.name