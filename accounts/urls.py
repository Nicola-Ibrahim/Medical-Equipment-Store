
from django.urls import path
from .views import WarehouseListView


urlpatterns = [
    path("warehouses_list/", WarehouseListView.as_view(), name="warehouse-list"),
]
