"""
Вьюшки для приложения mailing_service.
"""

from random import random

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy

from blog.models import Blog

from mailing_service.models import Client, Message, MailingSetting, LogsMessage
from mailing_service.forms import MessageForm, ClientForm, MailingModeratorForm, MailingSettingsForm
from mailing_service.services import get_cache_mailing_count, get_cache_mailing_active


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    extra_context = {
        'title': 'Список клиентов'
    }
    
    def get_queryset(self, *ard, **kwargs):
        queryset = super().get_queryset(*ard, **kwargs)
        
        if self.request.user.has_perm('mailing_service.can_view'):
            return queryset
        return queryset.filter(owner=self.request.user)


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
        blog_list = list(Blog.objects.all())
        if len(blog_list) > 3:
            random.shuffle(blog_list)
            context_data['blog_list'] = blog_list[:3]
        else:
            context_data['blog_list'] = blog_list

        return context_data


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailing_service/message_list.html'
    extra_context = {
        'title': 'Список сообщений'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if self.request.user.has_perm('mailing_service.can_view'):
            return queryset
        return queryset.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing_service:message_list')
    extra_context = {
        'title': 'Создание сообщения'
    }

    def form_valid(self, form):
        new_message = form.save()
        new_message.owner = self.request.user
        new_message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing_service:message_list')


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing_service:message_list')

    def test_func(self):
        if self.request.user == self.get_object().owner:
            return True
        return self.handle_no_permission()


class LogsMessageListView(ListView):
    model = LogsMessage
    template_name = 'mailing_service/logs_list.html'
    extra_context = {
        'title': 'Логи рассылок'
    }


class MailingSettingsListView(LoginRequiredMixin, ListView):
    model = MailingSetting
    template_name = 'mailing_service/mailing_settings_list.html'
    extra_context = {
        'title': 'Список рассылок'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if self.request.user.has_perm('mailing_service.can_view'):
            return queryset
        return queryset.filter(owner=self.request.user)


class MailingSettingsCreateView(LoginRequiredMixin, CreateView):
    model = MailingSetting
    form_class = MailingSettingsForm
    template_name = 'mailing_service/mailing_settings_form.html'
    success_url = reverse_lazy('mailing_service:mailing_settings_list')
    extra_context = {
        'title': 'Создание рассылки'
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form, *args, **kwargs):
        new_mailing = form.save(commit=False)
        new_mailing.owner = self.request.user
        new_mailing.save()
        return super().form_valid(form)


class MailingSettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingSetting
    form_class = MailingSettingsForm
    template_name = 'mailing_service/mailing_settings_form.html'
    success_url = reverse_lazy('mailing_service:mailing_settings_list')

    def get_form_class(self):
        if self.request.user == self.get_object().owner:
            return MailingSettingsForm
        elif self.request.user.has_perm('mailing_service.set_is_activated'):
            return MailingModeratorForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MailingSettingsDetailView(LoginRequiredMixin, DetailView):
    model = MailingSetting
    template_name = 'mailing_service/mailing_settings_detail.html'
    success_url = reverse_lazy('mailing_service:mailing_settings_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['clients'] = list(self.object.clients.all())
        context_data['logs'] = list(LogsMessage.objects.filter(mailing=self.object))
        return context_data


class MailingSettingsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MailingSetting
    template_name = 'mailing_service/mailing_settings_confirm_delete.html'
    success_url = reverse_lazy('mailing_service:mailing_settings_list')

    def test_func(self):
        _user = self.request.user
        if _user == self.get_object().owner or _user.has_perms(['mailing_service.can_delete', ]):
            return True
        return self.handle_no_permission()
