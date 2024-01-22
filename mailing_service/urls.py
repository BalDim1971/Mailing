"""
URL конфигурация для приложения mailing_service.

"""

from django.urls import path
from mailing_service.apps import MailingServiceConfig
from mailing_service.views import ClientListView, ClientCreateView, ClientDetailView, ClientUpdateView, ClientDeleteView

app_name = MailingServiceConfig.name


urlpatterns = [
    path('', ClientListView.as_view(), name='client_list'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client_view/<int:pk>', ClientDetailView.as_view(), name='client_view'),
    path('client_edit/<int:pk>', ClientUpdateView.as_view(), name='client_edit'),
    path('client_delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
]
