from django.contrib import admin
from .models import CustomUser, Child
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    ordering = ['email']
    
admin.site.register(Child)