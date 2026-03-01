import datetime

from django.contrib.auth.models import UserManager


class UserRelatedManager(UserManager):
    def get_by_otp(self, otp: str):
        return self.get(otp=otp, is_used=False, expires_at__gte=datetime.datetime.now(datetime.UTC))
