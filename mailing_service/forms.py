"""
Описание форм по работе с рассылками
"""

from django import forms
from django.forms import DateTimeInput

from mailing_service.models import Client, MailingSetting, Message, LogsMessage


class StyleFormMixin:
    """
    Общий класс для стилизации форм
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['is_active', 'email_verified', 'is_phone']:
                field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFormMixin, forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        """Стилизация формы"""
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["client"].queryset = Client.objects.filter(owner=user)
        self.fields["message"].queryset = Message.objects.filter(owner=user)
    
    class Meta:
        model = MailingSetting
        exclude = ('next_date', 'owner', 'status', 'is_activated',)
        
        widgets = {
            'start_date': DateTimeInput(attrs={'placeholder': 'ДД.ММ.ГГГГ ЧЧ:ММ:СС', 'type': 'datetime-local'}),
            'finish_date': DateTimeInput(attrs={'placeholder': 'ДД.ММ.ГГГГ ЧЧ:ММ:СС', 'type': 'datetime-local'}),
        }


class MailingModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingSetting
        fields = ('is_activated',)


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('owner',)


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('owner',)
