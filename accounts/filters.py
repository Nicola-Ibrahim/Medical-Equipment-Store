
import django_filters.rest_framework as filters
from .models import Warehouse


class WarehousesFilter(filters.FilterSet):

    # min_price = filters.NumberFilter(field_name="total_price", lookup_expr='gte')
    # max_price = filters.NumberFilter(field_name="total_price", lookup_expr='lte') 

    class Meta:
        model = Warehouse
        fields = {
            'warehouse_profile__name': ['icontains'], 
            "warehouse_profile__service": ['icontains', 'exact'],
            }