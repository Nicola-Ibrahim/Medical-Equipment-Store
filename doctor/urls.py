
from django.urls import path
from .views import OrdersListView, OrderRetrieveView


urlpatterns = [
    path("orders_list/", OrdersListView.as_view(), name="orders-list"),
    path("order_details/<int:pk>", OrderRetrieveView.as_view(), name="order-detail"),
]
