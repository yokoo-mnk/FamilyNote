from django import forms
from .models import SchoolLetter
from accounts.models import Child
from families.models import Family
from django.conf import settings

class SchoolLetterForm(forms.ModelForm):
    class Meta:
        model = SchoolLetter
        fields = ['child', 'title', 'image']
        labels = {
            'child': 'こどもの名前',
            'title': 'おたよりの名前',
            'image': 'おたより画像',
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)
        
        if user and user.family:
            self.fields['child'].queryset = Child.objects.filter(family=user.family)
            self.fields['child'].label_from_instance = lambda obj: obj.child_name