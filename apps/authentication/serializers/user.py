from django.contrib.auth.models import Group
from rest_framework_json_api import serializers

from apps.authentication.models import User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["name"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserBasicSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ["first_name", "email", "groups", "is_staff"]

class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    expires_in = serializers.IntegerField(read_only=True)

class UserLoginSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    token = TokenSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["first_name", "email", "groups", "is_staff", "token"]

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
