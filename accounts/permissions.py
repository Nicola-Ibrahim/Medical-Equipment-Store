from rest_framework import permissions
import enum

class PermissionGroupsName(enum.Enum):
    WAREHOUSE_GROUP = "warehouses_group"
    DOCTOR_GROUP = "doctors_group"

class CustomDjangoModelPermission(permissions.DjangoModelPermissions):
    perms_map = {
            'GET': ['%(app_label)s.view_%(model_name)s'],
            'OPTIONS': [],
            'HEAD': [],
            'POST': ['%(app_label)s.add_%(model_name)s'],
            'PUT': ['%(app_label)s.change_%(model_name)s'],
            'PATCH': ['%(app_label)s.change_%(model_name)s'],
            'DELETE': ['%(app_label)s.delete_%(model_name)s'],
        }



        
