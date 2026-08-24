import datetime

from django.conf import settings
from django.db import models
from rest_framework.authtoken.models import Token


class TokenWithRefresh(Token):
    expired_in = models.DateTimeField()
    refresh_token = models.CharField(max_length=40)

    def save(self, *args, **kwargs):
        self.expired_in = datetime.datetime.now() + datetime.timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS)
        self.expired_in = self.expired_in.replace(tzinfo=datetime.timezone.utc)
        self.refresh_token = self.generate_key()
        super().save(*args, **kwargs)

    def is_expired(self):
        return datetime.datetime.now(datetime.UTC) > self.expired_in
