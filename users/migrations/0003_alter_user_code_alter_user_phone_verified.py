# Generated by Django 5.0.1 on 2024-01-27 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_options_user_is_phone_user_phone_verified_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='code',
            field=models.CharField(blank=True, default='289103791534', max_length=50, null=True, verbose_name='проверочный код'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_verified',
            field=models.CharField(blank=True, default=models.CharField(blank=True, default='289103791534', max_length=50, null=True, verbose_name='проверочный код'), max_length=50, null=True, verbose_name='проверочный код телефона'),
        ),
    ]