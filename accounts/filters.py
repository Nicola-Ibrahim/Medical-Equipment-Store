
import django_filters.rest_framework as filters
from .models import Warehouse


class WarehousesFilter(filters.FilterSet):

    class Meta:
        model = Warehouse
        fields = {
            'warehouse_profile__name': ['icontains'], 
            "warehouse_profile__sections__name": ['icontains', 'exact'],
            }