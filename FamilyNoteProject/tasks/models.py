from django.db import models
from django.conf import settings

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
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True)
    due_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    title = models.CharField(max_length=100)
    memo = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to='task_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title