from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Product 
from .serializers import ProductSerializer
from accounts.mixins import PermissionMixin
from .mixins import WarehouseQuerySetMixin

# Create your views here.
class ProductsListView(
    PermissionMixin,
    WarehouseQuerySetMixin,
    ListCreateAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductRetrieveView(
    PermissionMixin,
    RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'


