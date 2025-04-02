from django import forms
from .models import SchoolLetter
from accounts.models import Child
from families.models import Family

class SchoolLetterForm(forms.ModelForm):
    class Meta:
        model = SchoolLetter
        fields = ['child', 'title', 'image']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)
        
        families = user.families.all()
        
        self.fields['child'].queryset = Child.objects.filter(family__in=families)