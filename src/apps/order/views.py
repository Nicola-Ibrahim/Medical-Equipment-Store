from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)

from apps.accounts.api.mixins import PermissionMixin

from .mixin import OrderQuerySetMixin
from .models import Order
from .serializers import OrderSerializer


class OrdersListView(PermissionMixin, OrderQuerySetMixin, ListCreateAPIView):

    """
    This view displays orders and creates a new one.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetailsView(PermissionMixin, RetrieveUpdateDestroyAPIView):
    """
    This view retrieves an order and allow editing and deleting it.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
