import enum

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN

from .errors import DeleteMultipleUsers
from .models import User

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


class PermissionGroupsName(enum.Enum):
    WAREHOUSE_GROUP = "warehouses_group"
    DOCTOR_GROUP = "doctors_group"


class BasePermission(permissions.DjangoModelPermissions):
    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }


class DeleteUserPermission(permissions.DjangoObjectPermissions):
    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }

    def has_object_permission(self, request, view, obj):
        """Override the has_object_permission for adding more constraints on users

        Args:
            request (_type_): _description_
            view (_type_): _description_
            obj (_type_): _description_

        Raises:
            Response: HTTP_403_FORBIDDEN
            Response: HTTP_403_FORBIDDEN
            DeleteMultipleUsers: Delete multiple user exception

        Returns:
            _type_: _description_
        """

        # authentication checks have already executed via has_permission
        queryset = self._queryset(view)
        model_cls = queryset.model
        user = request.user
        ids = request.data["ids"]

        # Get the user's permission related to the Http method
        perms = self.get_required_object_permissions(request.method, model_cls)

        if not user.has_perms(perms):
            # If the user does not have permissions we need to determine if
            # they have read permissions to see 403, or not, and simply see
            # a 404 response.

            if request.method in SAFE_METHODS:
                # Read permissions already checked and failed, no need
                # to make another lookup.
                raise Response(status=HTTP_403_FORBIDDEN)

            read_perms = self.get_required_object_permissions("GET", model_cls)
            if not user.has_perms(read_perms, obj):
                raise Response(status=HTTP_403_FORBIDDEN)

            # Has read permissions.
            return False

        if user.type != User.Type.ADMIN:

            # Prevent the non admin user from multiple deleting
            if len(ids) > 1:
                raise DeleteMultipleUsers()

            # Prevent
            if len(ids) == 1 and user.id == ids[0]:
                return True

            return False

        return True
