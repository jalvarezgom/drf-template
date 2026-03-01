from celery import shared_task
from apps.core.services.email import EmailService


@shared_task()
def ping_celery():
    response = EmailService.send_email__ping_celery()
    return response
