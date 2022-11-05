from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Product 
from .serializers import ProductSerializer
from accounts.mixins import WarehousePermissionMixin

# Create your views here.
class ProductsListView(
    WarehousePermissionMixin,
    ListCreateAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []


class ProductRetrieveView(
    WarehousePermissionMixin,
    RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'


