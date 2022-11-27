
from django.urls import path
from .views import *

app_name='order'

urlpatterns = [
    path("orders_list/", OrdersListView.as_view(), name="orders-list"),
    path("order_details/<int:pk>/", OrderDetailsView.as_view(), name="order-details"),
]
