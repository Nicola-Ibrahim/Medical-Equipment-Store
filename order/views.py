from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, UpdateAPIView
from .models import Order 
from .serializers import OrderSerializer 
from .mixin import OrderQuerySetMixin
from accounts.mixins import PermissionMixin

class OrdersListView(
    PermissionMixin,
    OrderQuerySetMixin,
    ListCreateAPIView):

    """
    This view displays orders and creates a new one.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer



class OrderDetailsView(
    PermissionMixin,
    RetrieveUpdateDestroyAPIView):
    """
    This view retrieves an order and allow editing and deleting it.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
