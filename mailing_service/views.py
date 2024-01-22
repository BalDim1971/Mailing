from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from mailing_service.models import Client


class ClientListView(ListView):
    model = Client
    extra_context = {
        'title': 'Список клиентов'
    }
    
    def get_queryset(self, *ard, **kwargs):
        queryset = super().get_queryset(*ard, **kwargs)
        
        return queryset


class ClientCreateView(CreateView):
    model = Client
    fields = ('last_name', 'first_name', 'patronymic', 'email', 'comments')
    success_url = reverse_lazy('mailing_service:client_list')
    extra_context = {
        'title': 'Новый клиент'
    }
    
    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.save()
        return super().form_valid(form)


class ClientDetailView(DetailView):
    model = Client
    success_url = reverse_lazy('mailing_service:client_list')
    extra_context = {
        'title': 'Подробная информация'
    }
    
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.save()
        return self.object


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('last_name', 'first_name', 'patronymic', 'email', 'comments')
    extra_context = {
        'title': 'Изменяем данные'
    }
    
    def get_success_url(self):
        return reverse('mailing_service:client_view', args=[self.kwargs.get('pk')])


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing_service:client_list')
