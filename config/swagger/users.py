from http import HTTPStatus

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample
from rest_framework_json_api import serializers

from apps.authentication.serializers.user import UserBasicSerializer, UserUpdateSerializer
from config.swagger import SwaggerTagEnum

users_viewset_swagger = extend_schema_view(
    get_profile=extend_schema(
        summary="Get user profile",
        description="Get user profile",
        tags=[SwaggerTagEnum.USERS],
        responses={
            HTTPStatus.OK: UserBasicSerializer,
        },
    ),
    update_profile=extend_schema(
        summary="Update user profile",
        description="Update user profile",
        tags=[SwaggerTagEnum.USERS],
        request=UserUpdateSerializer,
        responses={HTTPStatus.OK: UserBasicSerializer},
    ),
    deactivate=extend_schema(
        summary="Deactivate user",
        description="Deactivate user",
        tags=[SwaggerTagEnum.USERS],
        responses={
            HTTPStatus.ACCEPTED: OpenApiResponse(
                response=type("DeactivateResponse", (serializers.Serializer,), {}),
                description="User deactivated",
                examples=[OpenApiExample("Response Example", value={})],
            )
        },
    ),
)
