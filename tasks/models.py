from django.db import models
from django.contrib.auth import get_user_model
from families.models import Family
from django.conf import settings

User = get_user_model()

class Task(models.Model):
    CATEGORY_CHOICES = [
        ('shopping', '買い物'),
        ('cooking', '料理'),
        ('washing', '洗濯'),
        ('cleaning', '掃除'),
        ('hospital', '通院予定'),
        ('event', '行事予定'),
        ('other', 'その他'),
    ]
    
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="tasks")
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True)
    due_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='task_images/', blank=True, null=True)
    show_on_home = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='assigned_tasks'
    )
    is_all_assigned = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title