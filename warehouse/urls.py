
from django.urls import path
from .views import ProductsListView, ProductRetrieveView, WarehouseOrdersListView, WarehouseOrdersUpdateView


app_name = 'warehouse'

urlpatterns = [
    path("products_list/", ProductsListView.as_view(), name="products-list"),
    path("product_details/<slug:slug>", ProductRetrieveView.as_view(), name="product-detail"),
    path("orders_list/", WarehouseOrdersListView.as_view(), name="orders-list"),
    path("order_update/<int:pk>/", WarehouseOrdersUpdateView.as_view(), name="order-update"),
]
