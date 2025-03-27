from django import forms
from .models import User, Child
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class RegistForm(forms.ModelForm):
    password1 = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput(),
        min_length=8,
        help_text='8文字以上のパスワードを入力してください。',
    )
    password2 = forms.CharField(
        label='パスワード再入力',
        widget=forms.PasswordInput(),
        min_length=8,
        help_text='確認のため、パスワードをもう一度入力してください。',
    )
    nickname = forms.CharField(
        label='ニックネーム',
        max_length=30,
        help_text='アプリ内で使用する名前となります。 <br>例：ママ、パパ、おばあちゃん、じいじ など',
    )
    
    class Meta:
        model = User
        fields = ['username', 'nickname', 'email']
        labels = {
            'username': '名前',
            'nickname': 'ニックネーム',
            'email': 'メールアドレス',
        }
        
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
    
        if password1 and password2:
            if password1 != password2:
                raise ValidationError('パスワードとパスワード再入力が一致しません。')

        return cleaned_data
    
    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password1'], user)
        user.set_password(self.cleaned_data['password1'])
        user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "nickname", "email"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['name', 'birthdate']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_image']