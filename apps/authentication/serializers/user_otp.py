from rest_framework import serializers

from apps.authentication.models.user_otp import UserOTP


class UserOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOTP
        fields = "__all__"
