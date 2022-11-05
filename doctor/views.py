from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Order 
from .serializers import OrderSerializer
from accounts.mixins import WarehousePermissionMixin

# Create your views here.
class OrdersListView(
    ListCreateAPIView):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderRetrieveView(
    RetrieveUpdateDestroyAPIView):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer


