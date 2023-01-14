from rest_framework import permissions

from .factories import FilterFactory, UserTypeModelFactory, UserTypeSerializerFactory
from .permissions import CustomDjangoModelPermission


class PermissionMixin:
    permission_classes = [CustomDjangoModelPermission, permissions.IsAuthenticated]


class QuerySetMixin:
    def get_queryset(self):

        model_factory = UserTypeModelFactory()
        model = model_factory.get_suitable_model(self.request.query_params.get("type"))
        queryset = model.objects.all()
        return queryset


class SerializerParamsMixin:
    def get_serializer_class(self):
        """
        Override method to get serializer_class depending on the url parameters
        """
        serializer_factory = UserTypeSerializerFactory()
        serializer_class = serializer_factory.get_suitable_serializer(
            self.request.query_params.get("type")
        )

        return serializer_class


class UserTypeSerializerMixin:
    def get_serializer_class(self):
        """
        Override method to get serializer_class depending on the url parameters
        """
        # Change the serializer depending on the authenticated user type
        serializer_factory = UserTypeSerializerFactory()
        serializer_class = serializer_factory.get_suitable_serializer(
            self.request.user.type.lower()
        )

        return serializer_class


class FilterMixin:
    filter_backends = [
        FilterFactory,
    ]

    def filter_queryset(self, queryset):
        """
        Given a queryset, filter it with whichever filter backend is in use.

        You are unlikely to want to override this method, although you may need
        to call it either from a list view, or from a custom `get_object`
        method if you want to apply the configured filtering backend to the
        default queryset.
        """
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset
