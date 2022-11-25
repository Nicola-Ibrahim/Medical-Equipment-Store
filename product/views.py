from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, UpdateAPIView

from .models import Product 
from .serializers import ProductSerializer, ProductsSoldSerializer
from .mixins import ProductQuerySetMixin, ProductsSoldQuerySetMixin


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


class ProductDetailsView(
    PermissionMixin,
    RetrieveUpdateDestroyAPIView):

    """
    Update and delete a product related to a warehouse
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'


class ProductsSoldListView(
    ProductsSoldQuerySetMixin,
    ListAPIView
    ):
    serializer_class = ProductsSoldSerializer