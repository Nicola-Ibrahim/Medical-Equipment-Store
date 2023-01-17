from __future__ import annotations

from rest_framework import permissions

from .factories import FilterFactory, UserTypeModelFactory, UserTypeSerializerFactory
from .permissions import CustomDjangoModelPermission


class PermissionMixin:
    permission_classes = [CustomDjangoModelPermission, permissions.IsAuthenticated]


class QuerySetMixin:
    def get_queryset(self):
        """
        Override method to get queryset depending on the url kwargs
        """

        # Create a model factory to create a suitable model
        model_factory = UserTypeModelFactory()

        # Get the model
        model = model_factory.get_suitable_model(self.kwargs["user_type"])

        queryset = model.objects.all()
        return queryset


class SerializerParamsMixin:
    def get_serializer_class(self):
        """
        Override method to get serializer_class depending on the url kwargs
        """
        # Create a serializer factory to create a suitable serializer
        serializer_factory = UserTypeSerializerFactory()

        # Get the serializer
        serializer_class = serializer_factory.get_suitable_serializer(
            self.kwargs["user_type"]
        )

        return serializer_class


class UserTypeSerializerMixin:
    def get_serializer_class(self):
        """
        Override method to get serializer_class depending on the url parameters
        """
        # Create a serializer factory to create a suitable serializer
        serializer_factory = UserTypeSerializerFactory()

        # Get the serializer
        serializer_class = serializer_factory.get_suitable_serializer(
            self.request.user.type.lower()
        )

        return serializer_class


class FilterMixin:

    filter_backends = [
        FilterFactory,
    ]
