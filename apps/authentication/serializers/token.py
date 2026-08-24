from rest_framework import serializers

from apps.authentication.models.token import TokenWithRefresh
from apps.core.classes.serializers.timestamp import TimestampField


class TokenSerializer(serializers.ModelSerializer):
    access_token = serializers.CharField(source="key")
    expired_in = TimestampField()

    class Meta:
        model = TokenWithRefresh
        fields = ["access_token", "expired_in", "refresh_token"]
