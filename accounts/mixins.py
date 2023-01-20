from __future__ import annotations

from rest_framework import permissions

from .factories import FilterFactory, UserTypeModelFactory, UserTypeSerializerFactory
from .permissions import CustomDjangoModelPermission


class PermissionMixin:
    permission_classes = [CustomDjangoModelPermission, permissions.IsAuthenticated]


class KwargUserTypeQuerySetMixin:
    def get_queryset(self):
        """
        Override method to get queryset depending on the url kwargs
        """

        # Get the model
        model = UserTypeModelFactory().get_suitable_model(self.kwargs["user_type"])
        print(model)
        queryset = model.objects.all()
        return queryset


class UserTypeQuerySetMixin:
    def get_queryset(self):
        """
        Override method to get queryset depending on the url kwargs
        """

        # Get the model
        model = UserTypeModelFactory().get_suitable_model(
            self.request.user.type.lower()
        )
        queryset = model.objects.all()
        return queryset


class KwargUserTypeSerializerMixin:
    def get_serializer_class(self):
        """
        Override method to get serializer_class depending on the url kwargs
        """

        # Get the serializer
        serializer_class = UserTypeSerializerFactory().get_suitable_serializer(
            self.kwargs["user_type"]
        )

        return serializer_class


class UserTypeSerializerMixin:
    def get_serializer_class(self):
        """
        Override method to get serializer_class depending on the url kwargs
        """

        # Get the serializer
        serializer_class = UserTypeSerializerFactory().get_suitable_serializer(
            self.request.user.type.lower()
        )

        return serializer_class


class FilterMixin:

    filter_backends = [
        FilterFactory,
    ]
