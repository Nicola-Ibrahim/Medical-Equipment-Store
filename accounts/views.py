from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import WarehouseSerializer
from .models import Warehouse

# Create your views here.
class WarehouseListView(
    ListCreateAPIView):

    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class WarehouseRetrieveView(
    RetrieveUpdateDestroyAPIView):

    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

