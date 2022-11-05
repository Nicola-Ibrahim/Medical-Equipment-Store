from .permissions import IsWarehousePermission
from rest_framework import permissions

class WarehousePermissionMixin():
    permission_classes = [IsWarehousePermission, permissions.IsAuthenticated]

