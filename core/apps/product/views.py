from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView

from core.apps.accounts.mixins import PermissionMixin

from .filters import ProductFilter
from .mixins import ProductQuerySetMixin, ProductsSoldQuerySetMixin
from .models import Product
from .serializers import ProductSerializer, ProductsSoldSerializer


# Create your views here.
class ProductsListView(PermissionMixin, ProductQuerySetMixin, ListCreateAPIView):
    """
    Display all related products to specific warehouse
    Create a new product instance
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]  # Send image-date and form-data

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['name', 'price']

    def perform_create(self, serializer):
        serializer.save(warehouse=self.context['request'].user)
        return super().perform_create(serializer)


class ProductDetailsView(PermissionMixin, RetrieveUpdateDestroyAPIView):
    """
    Update and delete a product related to a warehouse
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'


class ProductsSoldListView(ProductsSoldQuerySetMixin, ListAPIView):
    serializer_class = ProductsSoldSerializer
