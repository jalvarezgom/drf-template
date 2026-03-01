from celery import shared_task

from apps.core.services.email import EmailService


@shared_task()
def send_email_recover_password(locale: str, email: str, otp_code: str, first_name: str):
    response = EmailService.send_email__recover_password(locale, email, otp_code, first_name)
    return response


@shared_task()
def send_email_welcome(locale: str, email: str, first_name: str):
    response = EmailService.send_email__welcome(locale, email, first_name)
    return response


@shared_task()
def send_email_signup_referral(locale: str, email: str, reference_code: int, commercial_name: str):
    response = EmailService.send_email__signup_referral(locale, email, reference_code, commercial_name)
    return response
