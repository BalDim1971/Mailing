#########################################################################
'''
Модели данных по работе с рассылкой.
Клиент рассылки, настройка рассылки, сообщение рассылки, логи рассылки.
'''
from django.db import models

from config import settings


NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
	'''
	Клиент сервиса:
	— контактный email,
	— ФИО,
	— комментарий.
	'''
	
	last_name = models.CharField(max_length=50, verbose_name='фамилия')
	first_name = models.CharField(max_length=50, verbose_name='имя')
	patronymic = models.CharField(max_length=50, verbose_name='отчество', **NULLABLE)

	email = models.EmailField(max_length=200, verbose_name='контактный email', unique=True)
	comments = models.TextField(verbose_name='комментарии')
	
	def __str__(self):
		return f'{self.last_name} {self.first_name} {self.email}'
	
	class Meta:
		verbose_name = 'клиент'
		verbose_name_plural = 'клиенты'
		ordering = ('last_name', 'first_name', 'patronymic', )


class Message(models.Model):
	'''
	Сообщение для рассылки:
	— тема письма,
	— тело письма.
	'''
	
	title = models.CharField(max_length=100, verbose_name='тема рассылки')
	body = models.TextField(verbose_name='тело рассылки')
	
	def __str__(self):
		return f'{self.title}'
	
	class Meta:
		verbose_name = 'сообщение'
		verbose_name_plural = 'сообщения'
		ordering = ('title',)


class MailingSetting(models.Model):
	'''
	Рассылка (настройки):
	— время рассылки;
	— периодичность: раз в день, раз в неделю, раз в месяц;
	— статус рассылки: завершена, создана, запущена.
	'''
	
	FREQUENCY = [
		('DAY', 'раз в день'),
		('WEEK', 'раз в неделю'),
		('MONTH', 'раз в месяц')
	]
	
	STATUS = [
		('FINISH', 'завершена'),
		('CREATE', 'создана'),
		('START', 'запущена')
	]
	
	time = models.TimeField(auto_now_add=True, verbose_name='время рассылки')
	create_date = models.DateField(auto_now_add=True, verbose_name='дата создания')
	frequency = models.CharField(max_length=100, choices=FREQUENCY, verbose_name='периодичность')
	status = models.CharField(max_length=100, choices=STATUS, verbose_name='статус')
	client = models.ManyToManyField(Client, verbose_name='клиент', blank=True)
	message = models.ForeignKey(Message, on_delete=models.SET_NULL, verbose_name='сообщение', **NULLABLE)
	finish_date = models.DateField(verbose_name='дата завершения рассылки', default='2024-01-01')
	finish_time = models.TimeField(verbose_name='время завершения рассылки', default='00:00')
	
	class Meta:
		verbose_name = 'настройка рассылки'
		verbose_name_plural = 'настройки рассылок'


class LogsMessage(models.Model):
	'''
	Логи рассылки:
	— дата и время последней попытки;
	— статус попытки;
	— ответ почтового сервера, если он был.
	'''
	
	STATUS = [
		('Success', 'успешно'),
		('Failure', 'отказ')
	]
	
	date_time = models.DateTimeField(auto_now_add=True, verbose_name='дата и время отправки')
	status = models.CharField(max_length=50, choices=STATUS, verbose_name='статус попытки')
	server_response = models.TextField(verbose_name='ответ почтового сервера', **NULLABLE)
	mailing = models.ForeignKey(MailingSetting, on_delete=models.SET_NULL, verbose_name='лог рассылки', **NULLABLE)
	
	def __str__(self):
		return f''
		
	class Meta:
		verbose_name = 'лог рассылки'
		verbose_name_plural = 'логи рассылки'

#########################################################################
