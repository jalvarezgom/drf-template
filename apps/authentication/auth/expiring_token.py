from rest_framework.authentication import TokenAuthentication


from rest_framework.exceptions import AuthenticationFailed

from apps.authentication.models.token import TokenWithRefresh
from django.utils.translation import gettext_lazy as _


class ExpiringTokenAuthentication(TokenAuthentication):
    model = TokenWithRefresh

    @classmethod
    def is_token_expired(cls, token):
        return token.is_expired()

    def authenticate(self, request):
        auth_value = super().authenticate(request)
        request.AUTH_ORIGIN = self.__class__.__name__
        return auth_value

    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)
        if self.is_token_expired(token):
            raise AuthenticationFailed(_("Token is expired"))
        return user, token
