from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=30)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "nickname"]
    
    def __str__(self):
        return self.email




#ここから下は一旦保留
# from django.db import models
# from django.contrib.auth.models import(
#     AbstractBaseUser, BaseUserManager, PermissionsMixin
# )
# from django.contrib.auth import get_user_model
# from django.conf import settings
# from django.urls import reverse_lazy
# from django.utils import timezone
# import uuid

# class UserManager(BaseUserManager):
#     def create_user(self, username, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('メールアドレスを入力してください')
#         if not password:
#             raise ValueError('パスワードを入力してください')
        
#         email = self.normalize_email(email)
#         user = self.model(username=username, email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
    
#     def create_superuser(self, username, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
        
#         return self.create_user(username, email, password, **extra_fields)

#     def authenticate(self, email=None, password=None):
#         try:
#             user = self.get(email=email)
#             if user.check_password(password):
#                 return user
#         except self.model.DoesNotExist:
#             return None
#         return None
    
    
# class User(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=100, unique=True)
#     nickname = models.CharField(max_length=100)
#     email = models.EmailField(max_length=300, unique=True)
#     date_joined = models.DateTimeField(default=timezone.now)
#     profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
    
#     objects = UserManager()
    
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
    
    
# class Family(models.Model):
#     family_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
#     family_name = models.CharField(max_length=100)
#     inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_families')
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         unique_together = ('family_name', 'inviter')
        
#     def __str__(self):
#         return f"Family {self.family_id} - Invited by {self.inviter.username}"  


# class FamilyInvitation(models.Model):
#     family = models.ForeignKey('Family', on_delete=models.CASCADE, related_name='invitations')
#     inviter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_invitations')
#     invite_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_used = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Invite {self.invite_code} for {self.family.family_name}"
    

# class Child(models.Model):
#     name = models.CharField(max_length=100)
#     birthdate = models.DateField()
#     user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='children')
    
#     def __str__(self):
#         return self.name