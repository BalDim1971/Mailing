import random

from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}

code = ''.join([str(random.randint(0, 9)) for _ in range(12)])

ACTIVE_CHOICES = [
    (True, 'Активен'),
    (False, 'Неактивен'),
]


class User(AbstractUser):
    """
    Класс, описывающий модель пользователь
    Стандартная модель расширяется:
    «Аватар»,
    «Номер телефона»,
    «Страна».
    Авторизация меняется на email
    """
    
    username = None
    email = models.EmailField(max_length=200, verbose_name='электронная почта', unique=True)
    
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    
    is_active = models.BooleanField(default=True, choices=ACTIVE_CHOICES, verbose_name='активен')
    
    email_verified = models.CharField(max_length=50, default=code, verbose_name='проверочный код почты', **NULLABLE)
    is_email = models.BooleanField(default=False, verbose_name='почта проверена')
    
    phone_verified = models.CharField(max_length=50, default=code, verbose_name='проверочный код телефона', **NULLABLE)
    is_phone = models.BooleanField(default=True, choices=ACTIVE_CHOICES, verbose_name='телефон проверен')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        permissions = [
            ('set_is_active', 'Может блокировать пользователя'),
        ]
