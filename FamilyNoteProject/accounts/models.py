from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, blank=True)
    nickname = models.CharField(max_length=30)
    profile_image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
    family = models.ForeignKey('families.Family', on_delete=models.SET_NULL, null=True, blank=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]
    
    def __str__(self):
        return self.email
    
    
class Child(models.Model):
    child_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    family = models.ForeignKey(
        "families.Family",
        on_delete=models.CASCADE,
        related_name="children"
    )

    def __str__(self):
        return f"{self.child_name} ({self.birth_date})"
