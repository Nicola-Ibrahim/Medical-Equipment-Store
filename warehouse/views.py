from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Product 
from .serializers import ProductSerializer
from accounts.mixins import WarehousePermissionMixin
from .mixins import WarehouseQuerySetMixin

# Create your views here.
class ProductsListView(
    WarehousePermissionMixin,
    WarehouseQuerySetMixin,
    ListCreateAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductRetrieveView(
    WarehousePermissionMixin,
    RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'


