from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from config import settings
from mailing_service.apps import MailingServiceConfig
from mailing_service.views import ClientListView, ClientCreateView

app_name = MailingServiceConfig.name


urlpatterns = [
    path('', ClientListView.as_view(), name='client_list'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
]
