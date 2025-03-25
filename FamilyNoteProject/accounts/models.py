from django.db import models
from django.contrib.auth.models import(
    BaseUserManager,AbstractBaseUser,PermissionsMixin
)
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils import timezone
import uuid

class UserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('メールアドレスを入力してください')
        if not password:
            raise ValueError('パスワードを入力してください')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)
    
    
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, unique=True, null=False, blank=False)
    email = models.EmailField(max_length=300, unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    def get_absolute_url(self):
        return reverse_lazy('accounts:home')
    
    
class Family(models.Model):
    name = models.CharField(max_length=100)
    invite_url = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    members = models.ManyToManyField(User, related_name="families")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Child(models.Model):
    name = models.CharField(max_length=100)
    birthdate = models.DateField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='children')
    
    def __str__(self):
        return self.name