import logging
import time

from django_guid import get_guid

from apps.core.utils.http import get_client_ip

logger = logging.getLogger("API")


class ResponseLoggingMiddleware:
    """Logs relevant information about every outgoing response."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.monotonic()
        response = self.get_response(request)
        self._log_response(request, response, time.monotonic() - start_time)
        return response

    @staticmethod
    def _log_response(request, response, duration_seconds):
        user = getattr(request, "user", None)
        log = logger.warning if response.status_code >= 400 else logger.info
        log(
            "[Response] %s %s | status=%s | duration_ms=%.2f | ip=%s | user=%s | content_length=%s | guid=%s",
            request.method,
            request.get_full_path(),
            response.status_code,
            duration_seconds * 1000,
            get_client_ip(request),
            getattr(user, "email", None) or "anonymous",
            len(response.content) if hasattr(response, "content") else "-",
            get_guid(),
        )
