from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomMinimumLengthValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _('パスワードが短すぎます。%(min_length)d文字以上にしてください。'),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return _('パスワードは%(min_length)d文字以上である必要があります。') % {'min_length': self.min_length}