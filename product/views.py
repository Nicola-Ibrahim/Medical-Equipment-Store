from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, UpdateAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from django_filters.rest_framework import DjangoFilterBackend
from .models import Product 
from .serializers import ProductSerializer, ProductsSoldSerializer
from .mixins import ProductQuerySetMixin, ProductsSoldQuerySetMixin
from .filters import ProductFilter
from accounts.mixins import PermissionMixin




# Create your views here.
class ProductsListView(
    # PermissionMixin,
    # ProductQuerySetMixin,
    ListCreateAPIView
    ):

    """
    Display all related products to specific warehouse
    Create a new product instance
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser] # Send image-date and form-data

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['name', 'price']



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


