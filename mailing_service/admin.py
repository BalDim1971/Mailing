#########################################################################
"""
Админский файл по работе с рассылкой.
Клиент рассылки, настройка рассылки, сообщение рассылки, логи рассылки.
"""

from django.contrib import admin
from mailing_service.models import Client, Message, MailingSetting, LogsMessage


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'patronymic', 'email', )
    list_filter = ('last_name', )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', )
    list_filter = ('title', )


@admin.register(MailingSetting)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'finish_date', 'frequency', 'status', 'owner', 'is_activated', )
    list_filter = ('message', )


@admin.register(LogsMessage)
class LogsMessageAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'date_time', 'status', )
    list_filter = ('status', )
