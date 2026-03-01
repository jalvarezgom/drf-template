from datetime import timedelta, datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.authentication.managers.otp import OTPManager


class UserOTP(models.Model):
    id = None
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    expires_at = models.DateTimeField()

    objects = OTPManager()

    class Meta:
        verbose_name = _("user_profile")
        verbose_name_plural = _("user_profiles")

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        if not self.expires_at:
            self.expires_at = self.created_at + timedelta(minutes=10)
        super().save(*args, **kwargs)
