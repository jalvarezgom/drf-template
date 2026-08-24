from django.contrib.auth.backends import ModelBackend
from django.core.cache import cache

from apps.authentication.models import User

RATE_LIMIT_MAX_ATTEMPTS = 5
RATE_LIMIT_WINDOW_SECONDS = 60


class SecretKeyBackend(ModelBackend):
    @staticmethod
    def _get_secret_key(request):
        return request.META.get("HTTP_X_SECRET_KEY", request.META.get("HTTP_SECRET_KEY", None))

    @staticmethod
    def _get_cache_key(request):
        ip = request.META.get("REMOTE_ADDR", "unknown")
        return f"secret-key-auth-attempts:{ip}"

    @classmethod
    def _is_rate_limited(cls, request):
        return cache.get(cls._get_cache_key(request), 0) >= RATE_LIMIT_MAX_ATTEMPTS

    @classmethod
    def _register_failed_attempt(cls, request):
        cache_key = cls._get_cache_key(request)
        attempts = cache.get(cache_key, 0)
        cache.set(cache_key, attempts + 1, RATE_LIMIT_WINDOW_SECONDS)

    def authenticate(self, request, **kwargs):
        secret_key = self._get_secret_key(request)
        if secret_key is None:
            return None
        if request is not None and self._is_rate_limited(request):
            return None
        try:
            user = User.objects.get(secret_key=secret_key)
            if self.user_can_authenticate(user) and user.secret_key is not None:
                return user
        except User.DoesNotExist:
            pass
        if request is not None:
            self._register_failed_attempt(request)
        return None
