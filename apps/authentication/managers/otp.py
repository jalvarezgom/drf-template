import datetime

from django.db import models


class OTPManager(models.Manager):
    def get_by_otp(self, otp: str):
        return self.get(otp=otp, is_used=False, expires_at__gte=datetime.datetime.now(datetime.UTC))
