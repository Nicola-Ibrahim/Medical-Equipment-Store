from __future__ import annotations

from rest_framework import permissions

from .factories import UserTypeFilterFactory, UserTypeModelFactory, UserTypeSerializerFactory
from .permissions import BasePermission, DeleteUserPermission, UpdateUserPermission


class PermissionMixin:
    permission_classes = [BasePermission, permissions.IsAuthenticated]


class DeleteUserPermissionMixin:
    permission_classes = [DeleteUserPermission, permissions.IsAuthenticated]


class UpdateUserPermissionMixin:
    permission_classes = [UpdateUserPermission, permissions.IsAuthenticated]


class KwargUserTypeQuerySetMixin:
    def get_queryset(self):
        """
        Override method to get queryset depending on the url kwargs
        """

        # Get the model
        model = UserTypeModelFactory().get_suitable_model(self.kwargs["user_type"])
        queryset = model.objects.all()
        return queryset


class InUserTypeQuerySetMixin:
    def get_queryset(self):
        """
        Override method to get queryset depending on the url kwargs
        """

        # Get the model
        model = UserTypeModelFactory().get_suitable_model(self.request.user.type.lower())
        queryset = model.objects.all()
        return queryset


class KwargUserTypeSerializerMixin:
    def get_serializer_class(self):
        """
        Override method to get serializer_class depending on the url kwargs
        """

        # Get the serializer
        serializer_class = UserTypeSerializerFactory().get_suitable_serializer(self.kwargs["user_type"])

        return serializer_class


class InUserTypeSerializerMixin:
    def get_serializer_class(self):
        """
        Override method to get serializer_class depending on the url kwargs
        """

        # Get the serializer
        serializer_class = UserTypeSerializerFactory().get_suitable_serializer(self.request.user.type.lower())

        return serializer_class


class FilterMixin:
    filter_backends = [
        UserTypeFilterFactory,
    ]
