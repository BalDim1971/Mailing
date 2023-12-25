from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from config import settings
from mailing_service.apps import MailingServiceConfig


app_name = MailingServiceConfig.name

urlpatterns = [

]
