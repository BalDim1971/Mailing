from django.db import models

from users.models import NULLABLE


class Blog(models.Model):
    """
    Класс, описывающий структуру Блогов (статей)
    """
    
    title = models.CharField(max_length=150, verbose_name='Наименование')
    body = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='blog/', verbose_name='Изображение', **NULLABLE)
    date_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    count_views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
