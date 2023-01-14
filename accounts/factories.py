from __future__ import annotations

from abc import ABC, abstractmethod

import django_filters.rest_framework as filters

from .errors import UserModelNotFound, UserSerializerNotFound
from .filters import DeliveryWorkerFilter, DoctorFilter, WarehouseFilter
from .models import DeliveryWorker, Doctor, User, Warehouse
from .serializers import (
    DeliveryWorkerUserSerializer,
    DoctorUserSerializer,
    UserSerializer,
    WarehouseUserSerializer,
)


class ModelFactory(ABC):
    @abstractmethod
    def get_suitable_model(self, type: str):
        pass


class UserTypeModelFactory(ModelFactory):
    def get_suitable_model(self, type: str) -> User:
        """Get the suitable serializer for user relying on its type

        Args:
            type (str): the type of model

        Raises:
            UserModelNotFound: model not found error

        Returns:
            User: model for register a user
        """

        models_classes = {
            "warehouse": Warehouse,
            "doctor": Doctor,
            "delivery_worker": DeliveryWorker,
        }

        model = models_classes.get(type, User)

        if not model:
            raise UserModelNotFound()

        return model


class SerializerFactory(ABC):
    @abstractmethod
    def get_suitable_serializer(self, type: str):
        pass


class UserTypeSerializerFactory(SerializerFactory):
    def get_suitable_serializer(self, type: str) -> UserSerializer:
        """Get the suitable serializer for user relying on its type

        Args:
            type (str): the type of serializer

        Raises:
            UserSerializerNotFound: serializer not found error

        Returns:
            UserSerializer: serializer for register a user
        """

        serializers_classes = {
            "warehouse": WarehouseUserSerializer,
            "doctor": DoctorUserSerializer,
            "delivery_worker": DeliveryWorkerUserSerializer,
        }

        serializer = serializers_classes.get(type, UserSerializer)

        if not serializer:
            raise UserSerializerNotFound()

        return serializer


class FilterFactory(filters.DjangoFilterBackend):
    def __init__(self) -> None:
        self.current_filter = None

    def get_suitable_filter(self, type: str) -> filters.FilterSet:
        """This a factory method to get the suitable filter for user registration

        Args:
            type (str): the type of filter

        Raises:
            UserFilterNotFound: filter not found error

        Returns:
            FilterSet: filter for register a user
        """

        serializers_classes = {
            "warehouse": WarehouseFilter,
            "doctor": DoctorFilter,
            "delivery_worker": DeliveryWorkerFilter,
        }

        filter_ = serializers_classes.get(type, None)

        # TODO: Repair the filter method, because it displays all users after processing

        # if not filter_:
        #     raise UserFilterNotFound()

        return filter_

    def get_filterset_class(self, view, queryset=None):
        """
        Return the `FilterSet` class used to filter the queryset.
        """
        filterset_class = self.get_suitable_filter(
            view.request.query_params.get("type")
        )
        filterset_fields = getattr(view, "filterset_fields", None)

        if filterset_class:
            filterset_model = filterset_class._meta.model

            # FilterSets do not need to specify a Meta class
            if filterset_model and queryset is not None:
                assert issubclass(
                    queryset.model, filterset_model
                ), "FilterSet model %s does not match queryset model %s" % (
                    filterset_model,
                    queryset.model,
                )

            return filterset_class
