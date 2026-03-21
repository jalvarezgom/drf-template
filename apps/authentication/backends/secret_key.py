from django.contrib.auth.backends import ModelBackend

from apps.authentication.models import User


class SecretKeyBackend(ModelBackend):
    @staticmethod
    def _get_secret_key(request):
        return request.META.get("HTTP_X_SECRET_KEY", request.META.get("HTTP_SECRET_KEY", None))

    def authenticate(self, request, **kwargs):
        secret_key = self._get_secret_key(request)
        if secret_key is None:
            return
        try:
            user = User.objects.get(secret_key=secret_key)
            if self.user_can_authenticate(user) and user.secret_key is not None:
                return user
        except User.DoesNotExist:
            return None
