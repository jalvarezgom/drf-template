from django.core.exceptions import (
    ValidationError,
)


class SpecialCharactersValidator:
    def __init__(self, min_special_characters=1):
        self.min_special_characters = min_special_characters

    def validate(self, password, user=None):
        special_characters_count = sum(1 for char in password if not char.isalnum())
        if special_characters_count < self.min_special_characters:
            raise ValidationError(
                f"This password must contain at least {self.min_special_characters} special character(s).",
                code="password_no_special_characters",
            )

    def get_help_text(self):
        return f"This password must contain at least {self.min_special_characters} special character(s)."


class UppercaseValidator:
    def __init__(self, min_uppercase=1):
        self.min_uppercase = min_uppercase

    def validate(self, password, user=None):
        uppercase_count = sum(1 for char in password if char.isupper())
        if uppercase_count < self.min_uppercase:
            raise ValidationError(
                f"This password must contain at least {self.min_uppercase} uppercase letter(s).",
                code="password_no_uppercase",
            )

    def get_help_text(self):
        return f"This password must contain at least {self.min_uppercase} uppercase letter(s)."


class LowercaseValidator:
    def __init__(self, min_lowercase=1):
        self.min_lowercase = min_lowercase

    def validate(self, password, user=None):
        lowercase_count = sum(1 for char in password if char.islower())
        if lowercase_count < self.min_lowercase:
            raise ValidationError(
                f"This password must contain at least {self.min_lowercase} lowercase letter(s).",
                code="password_no_lowercase",
            )

    def get_help_text(self):
        return f"This password must contain at least {self.min_lowercase} lowercase letter(s)."
