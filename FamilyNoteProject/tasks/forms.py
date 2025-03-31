from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        label='日付・期限（必須）',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    start_time = forms.TimeField(
        label='時間（任意）',
        required=False,
        widget=forms.TimeInput(attrs={'type': 'time'})
    )
    memo = forms.CharField(
        label='メモ（任意）',
        required=False,
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
            'memo': 'メモ（任意）',
            'image': '写真（任意）',
        }
        widgets = {
            "is_favorite": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
    
    def clean_start_time(self):
        start_time = self.cleaned_data.get('start_time')
        if start_time is None or start_time == '':
            return None  # 空欄の場合は None に設定
        return start_time