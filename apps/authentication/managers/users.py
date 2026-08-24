import datetime

from django.contrib.auth.models import UserManager


class UserRelatedManager(UserManager):
    def get_by_otp(self, otp: str):
        return self.get(
            userotp__otp=otp,
            userotp__is_used=False,
            userotp__expires_at__gte=datetime.datetime.now(datetime.UTC),
        )
