from django.core.exceptions import (
    ValidationError,
)

class NumericValidator:
    def __init__(self, min_numeric=0):
        self.min_numeric = min_numeric

    def validate(self, password, user=None):
        numeric_count = sum(c.isdigit() for c in password)
        if numeric_count < self.min_numeric:
            raise ValidationError(
                f"This password must contain at least {self.min_numeric} numeric character(s).",
                code="password_no_numeric",
            )

    def get_help_text(self):
        return f"Your password must contain at least {self.min_numeric} numeric character(s)."