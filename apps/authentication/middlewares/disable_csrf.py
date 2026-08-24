from django.utils.deprecation import MiddlewareMixin

from config.environment import Environment


class DisableCSRFMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if Environment.is_dev_mode():
            setattr(request, "_dont_enforce_csrf_checks", True)
