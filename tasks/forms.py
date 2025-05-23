from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        label='日付・期限（必須）',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    start_time = forms.TimeField(
        label='予定開始時間（任意）',
        required=False,
        widget=forms.TimeInput(attrs={'type': 'time'})
    )
    memo = forms.CharField(
        label='メモ（任意）',
        required=False,
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40})
    )
    category = forms.ChoiceField(
        choices=Task.CATEGORY_CHOICES,
        label='カテゴリ（必須）'
    )
    
    class Meta:
        model = Task
        fields = [ 
            'category', 'due_date', 'start_time', 'title', 'memo',
            'image',
        ]
        labels = {
            'category': 'カテゴリ（必須）',
            'due_date': '日付（必須）',
            'start_time': '予定開始時間（任意）',
            'title': 'タイトル（必須）',
            'memo': 'メモ（任意）',
            'image': '写真（任意）',
        }
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'image-field'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if not self.instance or not self.instance.image:
            self.fields['image'].required = False
            
    def clean_start_time(self):
        start_time = self.cleaned_data.get('start_time')
        if start_time is None or start_time == '':
            return None
        return start_time
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.image and not instance.image.name:
            instance.image.delete(save=False)
            instance.image = None

        if commit:
            instance.save()

        return instance