from http import HTTPStatus

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample
from rest_framework import serializers

from config.swagger import SwaggerTagEnum


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()


admin_viewset_swagger = extend_schema_view(
    clean_server_cache=extend_schema(
        summary="Clean server cache",
        description="Clean server cache",
        tags=[SwaggerTagEnum.ADMIN],
        responses={
            HTTPStatus.OK: OpenApiResponse(
                response=MessageSerializer,
                description="Cache cleaned",
                examples=[OpenApiExample("Response Example", value={"message": "Cache cleaned"})],
            ),
        },
    ),
)
