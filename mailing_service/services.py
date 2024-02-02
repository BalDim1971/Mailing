"""
Сервисные функции кэширования
и отправки рассылок
"""

from datetime import datetime, timedelta
import pytz
from django.core.cache import cache
from django.conf import settings
from mailing_service.models import MailingSetting, LogsMessage
from users.services import send_sms, send_mail_user


def my_job():
    day = timedelta(days=1)
    weak = timedelta(days=7)
    month = timedelta(days=28)
    
    mailings = MailingSetting.objects.all().filter(is_activated=True)
    
    today = datetime.now(pytz.timezone('Europe/Moscow'))
    mailings = mailings.filter(next_date__lte=today)
    
    for mailing in mailings:
        if mailing.status != 'FINISH':
            mailing.status = 'START'
            mailing.save()
            emails_list = [client.email for client in mailing.clients.all()]
            
            result = send_mail_user(
                subject=mailing.message.title,
                message=mailing.message.body,
                email_list=emails_list,
            )
            
            status = result == 1
            
            log = LogsMessage(mailing=mailing, status=status)
            log.save()
            
            if status:  # на случай сбоя рассылки она останется активной
                if mailing.next_date < mailing.finish_date:
                    mailing.status = 'CREATE'
                else:
                    mailing.status = 'FINISH'
            
            if mailing.interval == 'DAY':
                mailing.next_date = log.date_time + day
            elif mailing.interval == 'WEEK':
                mailing.next_date = log.date_time + weak
            elif mailing.interval == 'MONTH':
                mailing.next_date = log.date_time + month
            elif mailing.interval == 'ONCE':
                mailing.next_date = mailing.finish_date
            
            mailing.save()
            print(f'Рассылка {mailing.name} отправлена')
            # Рассылка по СМС
            phone_list = []
            for client in mailing.clients.all():
                if client.phone:
                    phone_list.append(client.phone)
            phone_str = '+'.join(phone_list)
            print(phone_str)
            sms_result = send_sms(phone=phone_str, message=mailing.message.body)
            print(f'СМС - {sms_result["status"]}')


def get_cache_mailing_count():
    """
    Получение/сохранение кэшированного списка рассылок
    :return: список рассылок
    """
    
    if settings.CACHE_ENABLED:
        key = 'mailings_count'
        mailings_count = cache.get(key)
        if mailings_count is None:
            mailings_count = MailingSetting.objects.all().count()
            cache.set(key, mailings_count, 3600)
    else:
        mailings_count = MailingSetting.objects.all().count()
    return mailings_count


def get_cache_mailing_active():
    """
    Получение/сохранение кэшированного списка активных рассылок
    :return: список активных рассылок
    """
    
    if settings.CACHE_ENABLED:
        key = 'active_mailings_count'
        active_mailings_count = cache.get(key)
        if active_mailings_count is None:
            active_mailings_count = MailingSetting.objects.filter(is_activated=True).count()
            cache.set(key, active_mailings_count, 3600)
    else:
        active_mailings_count = MailingSetting.objects.filter(is_activated=True).count()
    return active_mailings_count
