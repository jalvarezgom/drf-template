from celery import shared_task
from django_celery_beat.models import PeriodicTask

from apps.core.services.email import EmailService
from config.environment import Environment


@shared_task()
def demoAdd(x, y):
    Environment.logger.info(f"Adding {x} and {y}")
    return x + y


@shared_task()
def send_scheduled_email(subject, address):
    task = PeriodicTask.objects.get(name="send_scheduled_email")

    response = EmailService.send_email__demo(subject=subject, email=address, last_execution_date=task.last_run_at)

    return response
