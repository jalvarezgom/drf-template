from django.contrib.auth.backends import ModelBackend

from apps.authentication.models import User


class SecretKeyBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        secret_key = request.META.get("HTTP_SECRET_KEY", None)
        if secret_key is None:
            return
        try:
            user = User.objects.get(secret_key=secret_key)
            if self.user_can_authenticate(user) and user.secret_key is not None:
                return user
        except User.DoesNotExist:
            return None
