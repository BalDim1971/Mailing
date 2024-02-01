import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from mailing_service.models import Client, Message, MailingSetting, LogsMessage
from mailing_service.forms import MailingForm, MessageForm, ClientForm, MailingModeratorForm
from mailing_service.services import get_cache_mailing_count, get_cache_mailing_active

# from blog.models import blog


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    extra_context = {
        'title': 'Список клиентов'
    }
    
    def get_queryset(self, *ard, **kwargs):
        queryset = super().get_queryset(*ard, **kwargs)
        if self.request.user.has_perm('mailing_service.can_view'):
            return queryset
        return queryset.filter(owner='self.request.user')


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing_service:client_list')
    extra_context = {
        'title': 'Новый клиент'
    }
    
    def form_valid(self, form):
        new_client = form.save()
        new_client.owner = self.request.user
        new_client.save()
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
    form_class = ClientForm
    success_url = reverse_lazy('mailing_service:client_list')
    extra_context = {
        'title': 'Изменяем данные'
    }
    
    def test_func(self):
        return self.request.user == Client.objects.get(pk=self.kwargs['pk']).owner


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing_service:client_list')
    
    def test_func(self):
        permissions = ('mailing_service.client_delete',)
        _user = self.request.user
        _instance = self.get_object()
        if _user == _instance.owner or _user.has_perms(permissions):
            return True
        return self.handle_no_permission()


class HomeView(ListView):
    model = MailingSetting
    template_name = 'mailing_service/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['mailings_count'] = get_cache_mailing_count()
        context_data['active_mailings_count'] = get_cache_mailing_active()
        context_data['clients_count'] = len(Client.objects.all())
        # blog_list = list(blog.objects.all())
        # if len(blog_list) > 3:
        #     random.shuffle(blog_list)
        #     context_data['blog_list'] = blog_list[:3]
        # else:
        #     context_data['blog_list'] = []

        return context_data


class LogsListView(ListView):
    model = LogsMessage
    template_name = 'mailing_service/logs_list.html'
