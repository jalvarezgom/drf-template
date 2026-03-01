from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.utils.translation import override

from config.environment import Environment


class EmailService:
    @classmethod
    def send_email__recover_password(cls, locale: str, email: str, otp_code: str, first_name: str):
        landing_url = f"{Environment.SETTINGS.FRONTEND_URL.format(locale=locale)}"
        url = f"{Environment.SETTINGS.FRONTEND_URL.format(locale=locale)}/recover-password/{otp_code}"
        raise NotImplementedError("Revise email sending method for specific project needs.")
        with override(locale):
            response = Environment.EMAIL_MANAGER.send_email(
                subject=_("APP - Recover Password"),
                body=render_to_string(
                    "reset-password.html",
                    context={
                        "heading": _("Reset your password"),
                        "salutation": _("Hi %(first_name)s") % {"first_name": first_name},
                        "reset_request": _("We received a request to reset the password"),
                        "reset_how_to": _("To proceed with the authentication process"),
                        "reset_password": _("Reset password CTA"),
                        "link_copy_paste": _("If you cannot click on the above link"),
                        "time_limit": _("This link will be available for a limited time"),
                        "closing": _("Sincerely"),
                        "signature": _("APP – Account Security"),
                        "reset_url": url,
                        "landing_url": landing_url,
                    },
                ),
                to=[email],
                body_subtype="html",
            )
        return response

    @classmethod
    def send_email__welcome(cls, locale: str, email: str, first_name: str):
        landing_url = f"{Environment.SETTINGS.FRONTEND_URL.format(locale=locale)}"
        login_url = f"{Environment.SETTINGS.FRONTEND_URL.format(locale=locale)}/login"
        raise NotImplementedError("Revise email sending method for specific project needs.")
        with override(locale):
            response = Environment.EMAIL_MANAGER.send_email(
                subject=_("APP - Welcome!"),
                body=render_to_string(
                    "welcome.html",
                    context={
                        "heading": _("Welcome heading"),
                        "salutation": _("Hi %(first_name)s") % {"first_name": first_name},
                        "account_ready": _("Your APP account is ready"),
                        "access_platform": _("Access the platform"),
                        "enter_technical_details": _("Enter your project’s technical details"),
                        "questions": _("If you have any questions"),
                        "thanks": _("Thanks for joining us"),
                        "signature": _("APP | Certificados de Ahorro Energético Sostenible"),
                        "login_url": login_url,
                        "landing_url": landing_url,
                    },
                ),
                to=[email],
                body_subtype="html",
            )

        return response

    @classmethod
    def send_email__demo(cls, email: str, subject: str, last_execution_date):
        response = Environment.EMAIL_MANAGER.send_email(
            subject=subject,
            body=f"Esto es un email de prueba para las tareas periódicas. Esta tarea se ha ejecutado por última vez en {last_execution_date}",
            to=[email],
        )

        return response

    @classmethod
    def send_email__ping_celery(cls):
        project_name = "APP Backend"
        emails = []
        raise NotImplementedError("Revise email sending method for specific project needs.")
        response = Environment.EMAIL_MANAGER.send_email(
            subject=f"{project_name} -- Celery está en marcha",
            body=f"Esto es un email que se envía tras un despliegue de {project_name} para confirmar que el broker de Celery funciona correctamente. No necesitas tomar ninguna otra acción.",
            to=emails,
        )

        return response
