from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, UpdateAPIView

from .models import Product 
from .serializers import ProductSerializer, WarehouseOrdersSerializer, ProductsSoldSerializer
from .mixins import ProductQuerySetMixin, WarehouseOrdersQuerySetMixin, ProductsSoldQuerySetMixin


from accounts.mixins import PermissionMixin



# Create your views here.
class ProductsListView(
    PermissionMixin,
    ProductQuerySetMixin,
    ListCreateAPIView
    ):

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
    PermissionMixin,
    WarehouseOrdersQuerySetMixin,
    ListAPIView):

    """
    Obtain all related orders
    -----
    Make inner join between OrderProduct table 
    and Product table where warehouse == current user
    """
    serializer_class = WarehouseOrdersSerializer

    


class WarehouseOrdersUpdateView(
    PermissionMixin,
    WarehouseOrdersQuerySetMixin,
    UpdateAPIView
    ):

    """
    Obtain all related orders
    -----
    Make inner join between OrderProduct table 
    and Product table where warehouse == current user
    """
    serializer_class = WarehouseOrdersSerializer



class ProductsSoldListView(
    ProductsSoldQuerySetMixin,
    ListAPIView
    ):
    serializer_class = ProductsSoldSerializer