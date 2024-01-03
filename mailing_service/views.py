from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy, reverse

from mailing_service.models import Client


class ClientListView(ListView):
    model = Client
    extra_context = {
        'title': 'Сервер почтовых рассылок'
    }
    
    def get_queryset(self, *ard, **kwargs):
        queryset = super().get_queryset(*ard, **kwargs)
        
        return queryset


class ClientCreateView(CreateView):
    model = Client
    fields = ('last_name', 'first_name', 'patronymic',)
    success_url = reverse_lazy('mailing_service:list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.save()
        return super().form_valid(form)
