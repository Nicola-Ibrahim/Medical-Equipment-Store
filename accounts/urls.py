
from django.urls import path
from .views import WarehouseListView, WarehouseRetrieveView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = 'accounts'

urlpatterns = [
    path("warehouses_list/", WarehouseListView.as_view(), name="warehouses-list"),
    path("warehouse_detail/<int:pk>/", WarehouseRetrieveView.as_view(), name="warehouse-details"),


    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
