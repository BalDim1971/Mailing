from django.contrib import admin
from mailing_service.models import Client, Message, MailingSetting, LogsMessage


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'patronymic', )
    list_filter = ('last_name', )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_filter = ('title', )


@admin.register(MailingSetting)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('time', 'frequency', 'message', )
    list_filter = ('message', )


@admin.register(LogsMessage)
class LogsMessageAdmin(admin.ModelAdmin):
    list_display = ('date_time', 'status', 'mailing', )
    list_filter = ('status', )
