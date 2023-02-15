import django_filters.rest_framework as filters

from .models import Product


class ProductFilter(filters.FilterSet):

    product_name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    warehouse__warehouse_profile__name = filters.CharFilter(label='warehouse name', lookup_expr='icontains')
    warehouse__warehouse_profile__sections__name = filters.CharFilter(label='section', lookup_expr='icontains')

    class Meta:
        model = Product

        fields = []
