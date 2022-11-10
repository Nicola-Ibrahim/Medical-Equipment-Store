from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Order 
from .serializers import OrderSerializer
from .mixin import OrderQuerySetMixin
from accounts.mixins import PermissionMixin

# Create your views here.
class OrdersListView(
    PermissionMixin,
    OrderQuerySetMixin,
    ListCreateAPIView):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer



class OrderRetrieveView(
    PermissionMixin,
    RetrieveUpdateDestroyAPIView):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer


