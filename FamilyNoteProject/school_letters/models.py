from django.db import models
from accounts.models import Child

class SchoolLetter(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='school_letters')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='school_letters/images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.child.child_name}"