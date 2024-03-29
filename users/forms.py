from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from mailing_service.forms import StyleFormMixin
from users.models import User


class CustomUserCreationForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'password1', 'password2')


class UserProfileForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class ModeratorForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('is_active',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
