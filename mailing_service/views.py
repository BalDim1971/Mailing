from django.shortcuts import render
from django.views.generic import ListView

from mailing_service.models import Client


class ClientListView(ListView):
    model = Client
