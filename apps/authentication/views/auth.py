import random
from http import HTTPStatus
import time

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import transaction
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _


from apps.authentication.auth.expiring_token import ExpiringTokenAuthentication
from apps.authentication.backends.secret_key import SecretKeyBackend
from apps.authentication.models import User
from apps.authentication.models.token import TokenWithRefresh
from apps.authentication.models.user_otp import UserOTP
from apps.authentication.serializers.token import TokenSerializer
from apps.authentication.serializers.user import UserBasicSerializer, UserRegisterSerializer, UserLoginSerializer
from apps.authentication.tasks import send_email_recover_password
from apps.core.audit.audit_actions import AuditActionsRepository
from apps.core.utils.codes import generate_otp_code
from config.swagger.auth import auth_viewset_swagger


@auth_viewset_swagger
class AuthViewSet(viewsets.GenericViewSet):
    serializer_class = UserBasicSerializer

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        user = request.user
        return Response(UserBasicSerializer(user).data, status=HTTPStatus.OK)

    @action(detail=False, methods=["post"], permission_classes=[])
    def register(self, request):
        email = request.data.get("email")
        serializer = UserRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)

        is_valid, error = self.__is_password_valid(request.data.get("password"))
        if not is_valid:
            return Response({"password": error}, status=HTTPStatus.BAD_REQUEST)

        serializer.validated_data.update({"username": email})
        with transaction.atomic():
            user = User(**serializer.validated_data)
            user.set_password(request.data.get("password"))
            user.save()

        AuditActionsRepository.User.signup(user)
        return self.login(request)

    @action(detail=False, methods=["post"], permission_classes=[])
    def login(self, request):
        secret_key = self.request.META.get("HTTP_SECRET_KEY", None)
        if secret_key:
            response = self.__login_API(request)
        else:
            response = self.__login_credentials(request)
        return response

    def __login_credentials(self, request):
        user = authenticate(**request.data)
        ip = request.META.get("REMOTE_ADDR")
        if user and not user.is_anonymous:
            login(request, user)
        if not user or user.is_anonymous:
            AuditActionsRepository.User.login_failed(request.data, ip)
            return Response({"detail": _("Invalid Credentials or activate account")}, status=HTTPStatus.UNAUTHORIZED)
        token, created = TokenWithRefresh.objects.get_or_create(user=user)
        if ExpiringTokenAuthentication.is_token_expired(token):
            token.delete()
            token = TokenWithRefresh.objects.create(user=user)
        data = UserLoginSerializer(user).data
        data.update({"token": TokenSerializer(token).data})
        AuditActionsRepository.User.login_successful(user, ip)
        return Response(data=data, status=HTTPStatus.OK)

    def __login_API(self, request):
        user = SecretKeyBackend().authenticate(request)
        if user is not None:
            login(request, user, backend="api.authentication.backends.secret_key.SecretKeyBackend")
            return Response(status=HTTPStatus.OK)
        return Response({"error": _("Invalid credentials")}, status=HTTPStatus.UNAUTHORIZED)

    @action(detail=False, methods=["post"], url_path="refresh-token", permission_classes=[], authentication_classes=[])
    def refresh_token(self, request):
        refresh_token = request.data.get("refresh_token")
        token_str = request.headers.get("Authorization").split(" ")[-1]
        try:
            token = TokenWithRefresh.objects.get(key=token_str, refresh_token=refresh_token)
        except TokenWithRefresh.DoesNotExist:
            return Response({"detail": _("Invalid refresh token")}, status=HTTPStatus.UNAUTHORIZED)
        token.delete()
        token = TokenWithRefresh.objects.create(user=token.user)
        data = UserLoginSerializer(token.user).data
        data.update({"token": TokenSerializer(token).data})
        return Response(data=data, status=HTTPStatus.OK)

    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        request.user.auth_token.delete()
        return Response(status=HTTPStatus.ACCEPTED)

    @action(detail=False, methods=["post"], url_path="change-password", permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        user = request.user
        password = request.data.get("password")

        is_valid, error = self.__is_password_valid(password)
        if not is_valid:
            return Response({"password": error}, status=HTTPStatus.BAD_REQUEST)

        user.set_password(password)
        if not user.is_active:
            user.is_active = True
        user.save()
        return Response(status=HTTPStatus.ACCEPTED)

    @action(detail=False, methods=["post"], url_path="recover-password", permission_classes=[])
    def recover_password(self, request):
        email = request.data.get("email")
        try:
            EmailValidator()(email)
        except ValidationError:
            return Response({"detail": _("Invalid email")}, status=HTTPStatus.BAD_REQUEST)

        user = User.objects.filter(email=email)
        if user:
            otp = UserOTP()
            otp.user = user.first()
            otp.otp = generate_otp_code()
            otp.save()
            # TODO: 'send_email__recover_password' Migrate to Celeris
            send_email_recover_password.delay(settings.LANGUAGE_CODE, email, otp.otp, otp.user.first_name)
        else:
            time.sleep(random.uniform(0.4, 0.7))  # Avoid suspicious activity
        return Response({"detail": _("If the email exists, a password reset link will be sent")}, status=HTTPStatus.OK)

    @action(detail=False, methods=["post"], url_path="change-password-otp/(?P<otp>[0-9]+)", permission_classes=[])
    def change_password_otp(self, request, otp):
        try:
            user_otp = UserOTP.objects.get_by_otp(otp=otp)
        except UserOTP.DoesNotExist:
            return Response({"detail": _("Invalid OTP")}, status=HTTPStatus.BAD_REQUEST)
        if user_otp:
            user = user_otp.user
            password = request.data.get("password")

            is_valid, error = self.__is_password_valid(password)
            if not is_valid:
                return Response({"password": error}, status=HTTPStatus.BAD_REQUEST)

            user.set_password(password)
            if not user.is_active:
                user.is_active = True
            user.save()
            user_otp.is_used = True
            user_otp.save()
        return Response({"detail": _("Password changed successfully")}, status=HTTPStatus.ACCEPTED)

    def __is_password_valid(self, password):
        try:
            validate_password(password)
            return True, None
        except ValidationError as e:
            return False, e.messages
