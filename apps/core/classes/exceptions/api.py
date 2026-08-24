from rest_framework import status
from rest_framework.exceptions import APIException as APIExceptionDRF
from django.utils.translation import gettext_lazy as _


class APIException(APIExceptionDRF):
    """Base API exception class."""

    default_detail = None

    def __init__(self, detail=None, exc_type=None, code=None, **data):
        if not exc_type:
            exc_type = self.name
        self.detail = detail
        details = {"type": exc_type, "detail": self.get_message(), 'data': data}
        super(APIException, self).__init__(details, code)

    @property
    def name(self):
        return self.__class__.__name__

    def get_message(self):
        messages = [self.default_detail, self.detail]
        return " | ".join([str(m) for m in messages if m is not None])

    def __repr__(self):
        return self.get_message()


class NoDataAPIException(APIException):
    status_code = status.HTTP_204_NO_CONTENT
    default_detail = _("No data available for the requested resource.")


class NotFoundAPIException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _("The requested resource was not found.")


class InvalidActionAPIException(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = _("The request is invalid.")
