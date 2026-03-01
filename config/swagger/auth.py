from http import HTTPStatus

from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample, OpenApiRequest
from rest_framework_json_api import serializers

from apps.authentication.serializers.user import (
    UserBasicSerializer,
    UserRegisterSerializer,
    UserLoginSerializer,
)
from config.swagger import SwaggerTagEnum

auth_viewset_swagger = extend_schema_view(
    me=extend_schema(
        summary="Profile",
        description="User authenticated data",
        tags=[SwaggerTagEnum.AUTH],
        responses={HTTPStatus.OK: UserBasicSerializer},
    ),
    register=extend_schema(
        summary="Register",
        description="Register user and return login payload",
        tags=[SwaggerTagEnum.AUTH],
        request=UserRegisterSerializer,
        responses={HTTPStatus.OK: UserLoginSerializer},
    ),
    login=extend_schema(
        summary="Login",
        description="Login user (credentials) or use secret-key header for API login",
        tags=[SwaggerTagEnum.AUTH],
        request=type(
            "LoginRequestSerializer",
            (serializers.Serializer,),
            {"username": serializers.CharField(), "password": serializers.CharField(write_only=True)},
        ),
        responses={
            HTTPStatus.OK: UserLoginSerializer,
            HTTPStatus.UNAUTHORIZED: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Invalid credentials",
                examples=[OpenApiExample("Invalid Credentials Example", value={"detail": "Invalid Credentials or activate account"})],
            ),
        },
    ),
    refresh_token=extend_schema(
        summary="Refresh Token",
        description="Refresh user token using refresh_token and Authorization header with current access token",
        tags=[SwaggerTagEnum.AUTH],
        request=type(
            "RefreshTokenRequestSerializer",
            (serializers.Serializer,),
            {"refresh_token": serializers.CharField()},
        ),
        responses={HTTPStatus.OK: UserLoginSerializer},
    ),
    logout=extend_schema(
        summary="Logout",
        description="Logout authenticated user",
        tags=[SwaggerTagEnum.AUTH],
        responses={
            HTTPStatus.ACCEPTED: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Successful logout",
                examples=[OpenApiExample("Logout Response Example", value={})],
            ),
        },
    ),
    change_password=extend_schema(
        summary="Change password",
        description="Change password authenticated user",
        tags=[SwaggerTagEnum.AUTH],
        request=type("ChangePasswordSerializer", (serializers.Serializer,), {"password": serializers.CharField()}),
        responses={
            HTTPStatus.ACCEPTED: OpenApiResponse(
                response=OpenApiTypes.OBJECT, description="Password changed", examples=[OpenApiExample("Response Example", value={})]
            )
        },
    ),
    recover_password=extend_schema(
        summary="Recover password",
        description="Recover password",
        tags=[SwaggerTagEnum.AUTH],
        request=OpenApiRequest(
            request=OpenApiTypes.OBJECT,
            examples=[OpenApiExample("Recover Password Request Example", value={"email": "your-email"})],
        ),
        responses={
            HTTPStatus.OK: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Password recovered",
                examples=[OpenApiExample("Response Example", value={})],
            ),
        },
    ),
    change_password_otp=extend_schema(
        summary="Change password with OTP",
        description="Change password with OTP",
        tags=[SwaggerTagEnum.AUTH],
        request=type("ChangePasswordSerializerOTP", (serializers.Serializer,), {"password": serializers.CharField()}),
        responses={
            HTTPStatus.ACCEPTED: OpenApiResponse(
                response=OpenApiTypes.OBJECT, description="Password changed", examples=[OpenApiExample("Response Example", value={})]
            )
        },
    ),
)


class SecretKeyAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "apps.authentication.backends.secret_key.SecretKeyBackend"
    name = "X-SECRET-KEY"

    def get_security_definition(self, auto_schema):
        return {"type": "apiKey", "in": "meta", "name": "HTTP_SECRET_KEY"}
