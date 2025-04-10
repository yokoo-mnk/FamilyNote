from django.contrib.auth.models import AbstractUser
from django.db import models
from django.templatetags.static import static

from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password=None, **extra_fields):
        """
        Create and return a superuser with an email, nickname, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, nickname, password, **extra_fields)
    
    
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, blank=True)
    nickname = models.CharField(max_length=30)
    image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
    family = models.ForeignKey(
        'families.Family', on_delete=models.CASCADE, null=True, blank=True, related_name='members'
    )
    objects = CustomUserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]
    
    def __str__(self):
        return self.email
    
    @property
    def profile_image_url(self):
        if self.image:
            return self.image.url
        return static('accounts/images/default.png')
    
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
