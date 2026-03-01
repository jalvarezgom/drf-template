from django.db.models import JSONField
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def outer_json_is_object(value):
    if not isinstance(value, dict):
        raise ValidationError(_("Outer JSON item should be an object"), code="invalid_json_object")


class JSONIntKeyField(JSONField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        value = super().from_db_value(value, expression, connection)
        if value is not None:
            return {int(k): v for k, v in value.items()}
