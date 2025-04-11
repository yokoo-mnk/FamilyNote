from django.contrib import admin
from .models import CustomUser, Child
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('email', 'full_name', 'nickname', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('プロフィール情報', {'fields': ('full_name', 'nickname', 'image', 'family')}),
        ('権限', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('日付情報', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('email', 'nickname')
    ordering = ('email',)
    
admin.site.register(CustomUser, CustomUserAdmin)