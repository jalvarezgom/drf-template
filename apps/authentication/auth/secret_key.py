from rest_framework.authentication import BaseAuthentication


from rest_framework.exceptions import AuthenticationFailed

from apps.authentication.backends.secret_key import SecretKeyBackend
from django.utils.translation import gettext_lazy as _


class SecretKeyAuthentication(BaseAuthentication):
    __backend = SecretKeyBackend

    def authenticate(self, request):
        secret_key = request.META.get("HTTP_SECRET_KEY", None)
        if secret_key is None:
            return
        user = self.__backend().authenticate(request)
        if not user:
            raise AuthenticationFailed(_("Secret key is expired or not valid"))
        request.AUTH_ORIGIN = self.__class__.__name__
        return user, None
