#########################################################################
"""
Модели данных по работе с рассылкой.
Клиент рассылки, настройка рассылки, сообщение рассылки, логи рассылки.
"""

from django.db import models
from django.utils import timezone

import users.models
from users.models import NULLABLE


class Client(models.Model):
    """
    Клиент сервиса:
    — контактный email,
    — ФИО, полное + "фамилия и.о." ???
    — комментарий.
    """
    
    last_name = models.CharField(max_length=50, verbose_name='фамилия')
    first_name = models.CharField(max_length=50, verbose_name='имя')
    patronymic = models.CharField(max_length=50, verbose_name='отчество', **NULLABLE)
    
    email = models.EmailField(max_length=200, verbose_name='контактный email', unique=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон', **NULLABLE)
    
    comments = models.TextField(verbose_name='комментарии')
    
    owner = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True, verbose_name='отправитель')
    
    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.email}'
    
    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        ordering = ('last_name', 'first_name', 'patronymic',)
        permissions = [
            ('client_delete', 'Может удалять клиентов')
        ]


class Message(models.Model):
    """
    Сообщение для рассылки:
    — тема письма,
    — тело письма.
    """
    
    title = models.CharField(max_length=100, verbose_name='тема рассылки')
    body = models.TextField(verbose_name='тело рассылки')
    owner = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True, verbose_name='владелец сообщения')

    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ('title',)


class MailingSetting(models.Model):
    """
    Рассылка (настройка):
    — время рассылки;
    — периодичность: раз в день, раз в неделю, раз в месяц;
    — статус рассылки: завершена, создана, запущена.
    """
    
    FREQUENCY = [
        ('ONCE', 'разовая'),
        ('DAY', 'раз в день'),
        ('WEEK', 'раз в неделю'),
        ('MONTH', 'раз в месяц')
    ]
    
    STATUS = [
        ('FINISH', 'завершена'),
        ('CREATE', 'создана'),
        ('START', 'запущена')
    ]
    
    ACTIVE_CHOICES = [
        (True, 'Активна'),
        (False, 'Неактивна'),
    ]
    
    name = models.CharField(max_length=50, verbose_name='наименование рассылка', default='test')

    start_date = models.DateTimeField(default=timezone.now, verbose_name='начало рассылки')
    next_date = models.DateTimeField(default=timezone.now, verbose_name='следующая рассылка')
    finish_date = models.DateTimeField(verbose_name='завершение рассылки')

    frequency = models.CharField(default='ONCE', max_length=15, choices=FREQUENCY, verbose_name='периодичность')
    status = models.CharField(max_length=100, choices=STATUS, verbose_name='статус', default='CREATE')
    clients = models.ManyToManyField(Client, verbose_name='получатели', blank=True)
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, verbose_name='сообщение', **NULLABLE)
    owner = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True, verbose_name='владелец рассылки')
    
    is_activated = models.BooleanField(default=True, choices=ACTIVE_CHOICES, verbose_name='Активность')
    
    def __str__(self):
        return f'Рассылка {self.name}'
    
    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ('start_date',)
    
    permissions = [
        ('set_is_activated', 'Может отключать рассылку'),
        ('can_view', 'Может просматривать рассылки')
    ]


class LogsMessage(models.Model):
    """
    Логи рассылки:
    — дата и время последней попытки;
    — статус попытки;
    — ответ почтового сервера, если он был.
    """
    
    STATUS = [
        ('Success', 'успешно'),
        ('Failure', 'отказ')
    ]
    
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='дата и время отправки', **NULLABLE)
    status = models.CharField(max_length=50, choices=STATUS, verbose_name='статус попытки', **NULLABLE)
    server_response = models.TextField(verbose_name='ответ почтового сервера', **NULLABLE)
    mailing = models.ForeignKey(MailingSetting, on_delete=models.SET_NULL, verbose_name='лог рассылки', **NULLABLE)
    
    def __str__(self):
        return f'{self.date_time} - {self.status}'
    
    class Meta:
        verbose_name = 'лог рассылки'
        verbose_name_plural = 'логи рассылки'

#########################################################################
