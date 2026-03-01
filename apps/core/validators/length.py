from django.core.exceptions import (
    ValidationError,
)

class MaximumLengthValidator:
    def __init__(self, max_length=72):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                "This password is too long. It must contain at most %(max_length)d characters." % {
                    "max_length": self.max_length,
                },
                code="password_too_long",
            )

    def get_help_text(self):
        return "Your password must contain at most %(max_length)d characters." % {
            "max_length": self.max_length,
        }