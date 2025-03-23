from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        label='日付・期限（必須）',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    start_time = forms.TimeField(
        label='時間（任意）',
        widget=forms.TimeInput(attrs={'type': 'time'})
    )
    
    category = forms.ChoiceField(
        choices=Task.CATEGORY_CHOICES,
        label='カテゴリ（必須）'
    )
    
    class Meta:
        model = Task
        fields = [ 
            'category', 'due_date', 'start_time', 'title', 'memo', 'image'
        ]
        labels = {
            'category': 'カテゴリ（必須）',
            'due_date': '日付（必須）',
            'start_time': '時間（任意）',
            'title': 'タイトル（必須）',
            'memo': 'メモ（必須）',
            'image': '写真',
        }