import logging

from django_guid import get_guid

from apps.core.utils.http import get_client_ip

logger = logging.getLogger("API")


class RequestLoggingMiddleware:
    """Logs relevant information about every incoming request."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self._log_request(request)
        return self.get_response(request)

    @staticmethod
    def _log_request(request):
        logger.info(
            "[Request] %s %s | ip=%s | content_type=%s | content_length=%s | user_agent=%s | guid=%s",
            request.method,
            request.get_full_path(),
            get_client_ip(request),
            request.META.get("CONTENT_TYPE", "-"),
            request.META.get("CONTENT_LENGTH", "-"),
            request.META.get("HTTP_USER_AGENT", "-"),
            get_guid(),
        )
