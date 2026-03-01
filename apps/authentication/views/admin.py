from http import HTTPStatus

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.authentication.permissions.users import IsAdminUser
from config.swagger.admin import admin_viewset_swagger

from apps.core.serializers.empty import EmptySerializer


@admin_viewset_swagger
class AdminViewset(viewsets.GenericViewSet):
    def get_serializer_class(self):
        return EmptySerializer

    @action(detail=False, methods=["get"], permission_classes=[IsAdminUser])
    def clean_server_cache(self, request):
        return Response({"message": ""}, status=HTTPStatus.OK)
