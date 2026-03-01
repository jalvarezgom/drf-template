from django.contrib.auth.backends import ModelBackend

from apps.authentication.models import User


class EmailPasswordBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return
        try:
            user = User.objects.get(email=email)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
            return None
