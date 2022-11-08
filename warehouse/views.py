from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Product 
from .serializers import ProductSerializer, WarehouseOrdersSerializer
from .mixins import ProductQuerySetMixin, WarehouseOrdersQuerySetMixin

from accounts.mixins import PermissionMixin
from doctor.models import OrderProduct

# Create your views here.
class ProductsListView(
    PermissionMixin,
    ProductQuerySetMixin,
    ListCreateAPIView):

    """
    Display all related products to specific warehouse
    Create a new product instance
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductRetrieveView(
    PermissionMixin,
    RetrieveUpdateDestroyAPIView):

    """
    Update and delete a product related to a warehouse
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'


class WarehouseOrdersListView(
    WarehouseOrdersQuerySetMixin,
    ListCreateAPIView):

    """
    Obtain all related orders
    -----
    Make inner join between OrderProduct table 
    and Product table where warehouse == current user
    """

    queryset = OrderProduct.objects.all()
    serializer_class = WarehouseOrdersSerializer


    
