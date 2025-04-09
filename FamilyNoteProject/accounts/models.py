from django.contrib.auth.models import AbstractUser
from django.db import models
from django.templatetags.static import static


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, blank=True)
    nickname = models.CharField(max_length=30)
    image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
    family = models.ForeignKey(
        'families.Family', on_delete=models.CASCADE, null=True, blank=True, related_name='members'
    )
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]
    
    def __str__(self):
        return self.email
    
    @property
    def profile_image_url(self):
        if self.image:
            return self.image.url
        return static('images/default.png')
    
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
