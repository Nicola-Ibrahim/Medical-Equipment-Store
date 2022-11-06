from .permissions import CustomDjangoModelPermission
from rest_framework import permissions

class PermissionMixin():
    permission_classes = [CustomDjangoModelPermission, permissions.IsAuthenticated]

