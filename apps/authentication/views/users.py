from http import HTTPStatus

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.authentication.serializers.user import UserBasicSerializer, UserUpdateSerializer
from config.swagger.users import users_viewset_swagger


@users_viewset_swagger
class UsersViewSet(viewsets.GenericViewSet):
    serializer_class = UserBasicSerializer

    @action(detail=False, methods=["get"], url_path="get-profile", permission_classes=[permissions.IsAuthenticated])
    def get_profile(self, request):
        user = request.user
        return Response(UserBasicSerializer(user).data, status=HTTPStatus.OK)

    @action(detail=False, methods=["put"], url_path="update-profile", permission_classes=[permissions.IsAuthenticated])
    def update_profile(self, request):
        user = request.user
        serializer = UserUpdateSerializer(data=request.data, partial=True, instance=user)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
        serializer.save()
        return Response(UserBasicSerializer(user).data, status=HTTPStatus.OK)

    @action(detail=False, methods=["delete"], url_path="deactivate", permission_classes=[permissions.IsAuthenticated])
    def deactivate(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response(status=HTTPStatus.ACCEPTED)
