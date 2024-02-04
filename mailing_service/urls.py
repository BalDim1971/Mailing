"""
URL конфигурация для приложения mailing_service.
"""

from django.urls import path
from mailing_service.apps import MailingServiceConfig
from mailing_service.views import ClientListView, ClientCreateView, ClientDetailView, ClientUpdateView, \
    ClientDeleteView, HomeView, MailingSettingsListView, MailingSettingsCreateView, MessageListView, MessageCreateView, \
    MessageDetailView, MessageUpdateView, MessageDeleteView, MailingSettingsUpdateView, MailingSettingsDetailView, \
    MailingSettingsDeleteView, LogsMessageListView

app_name = MailingServiceConfig.name


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client_view/<int:pk>', ClientDetailView.as_view(), name='client_view'),
    path('client_edit/<int:pk>', ClientUpdateView.as_view(), name='client_edit'),
    path('client_delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_view/<int:pk>', MessageDetailView.as_view(), name='message_view'),
    path('message_edit/<int:pk>', MessageUpdateView.as_view(), name='message_edit'),
    path('message_delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
    path('mailing_settings_list/', MailingSettingsListView.as_view(), name='mailing_settings_list'),
    path('mailing_settings_create/', MailingSettingsCreateView.as_view(), name='mailing_settings_create'),
    path('mailing_settings_update/<int:pk>', MailingSettingsUpdateView.as_view(), name='mailing_settings_update'),
    path('mailing_settings_view/<int:pk>', MailingSettingsDetailView.as_view(), name='mailing_settings_view'),
    path('mailing_settings_delete/<int:pk>', MailingSettingsDeleteView.as_view(), name='mailing_settings_delete'),
    path('logs_list/', LogsMessageListView.as_view(), name='logs_list'),
]
