from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm, PasswordChangeForm,
)
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext as _

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="パスワード",
        strip=False,
        min_length=8,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="8文字以上のパスワードを入力してください。",
        error_messages={
            'required': 'パスワードは必須項目です。',
            'min_length': 'パスワードは最低8文字以上必要です。',
        },
    )
    password2 = forms.CharField(
        label="パスワード確認",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="確認のため、もう一度同じパスワードを入力してください。",
        error_messages={
            'required': 'パスワード確認は必須項目です。',
            'password_mismatch': 'パスワードが一致しません。',
        },
    )
    nickname = forms.CharField(
        label='ニックネーム（続柄）',
        max_length=30,
        help_text='アプリ内で使用する名前となります。 <br>例：ママ、パパ、おばあちゃん、じいじ など',
    )
    email = forms.EmailField(label="メールアドレス")
    full_name = forms.CharField(label="名前", max_length=50)
    
    class Meta:
        model = User
        fields = ["full_name", "nickname", "email", "password1", "password2"]

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='メールアドレス',
    )
    password = forms.CharField(
        label="パスワード",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="8文字以上のパスワードを入力してください。",
    )


class UserUpdateForm(forms.ModelForm):
    full_name = forms.CharField(label="名前", max_length=50)
    nickname = forms.CharField(label='ニックネーム（続柄）',max_length=30)
    email = forms.EmailField(label="メールアドレス")
    
    class Meta:
        model = User
        fields = ["full_name", "nickname", "email", "image"]
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'image-field'}),
        }
        labels = {
            "image": "プロフィール画像",
        }
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if self.cleaned_data.get('image') is None and self.files.get('image') is None:
            if self.data.get('image-clear') == 'on':
                if instance.image:
                    instance.image.delete(save=False)
                    instance.image = None 
        
        if commit:
            instance.save()

        return instance

class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="現在のパスワード")
    new_password = forms.CharField(widget=forms.PasswordInput, label="新しいパスワード")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="新しいパスワード（確認）")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if not self.user.check_password(old_password):
            raise ValidationError('現在のパスワードが正しくありません。')

        if new_password != confirm_password:
            raise ValidationError('新しいパスワードと確認用パスワードが一致しません。')

        try:
            validate_password(new_password, self.user)
        except ValidationError as e:
            messages = [msg for msg in e.messages if not msg.strip().startswith("This ")]
            if not messages:
                messages = [e.messages[0]]
            raise ValidationError(messages)

        return cleaned_data          