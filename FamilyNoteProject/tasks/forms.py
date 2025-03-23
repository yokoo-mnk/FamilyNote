from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [ 
            'category', 'due_date', 'time', 'title', 'memo', 'image'
        ]