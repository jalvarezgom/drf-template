from rest_framework import permissions
from django.utils.translation import gettext_lazy as _


class IsAdminUser(permissions.BasePermission):
    message = _("User is not an admin user")

    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.is_admin())
