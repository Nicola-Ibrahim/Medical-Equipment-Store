
from django.urls import path
from .views import WarehouseListView, WarehouseRetrieveView


app_name = 'accounts'

urlpatterns = [
    path("warehouses_list/", WarehouseListView.as_view(), name="warehouses-list"),
    path("warehouse_detail/<int:pk>/", WarehouseRetrieveView.as_view(), name="warehouse-details"),
]
