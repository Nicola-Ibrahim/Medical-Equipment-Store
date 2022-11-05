
from django.urls import path
from .views import ProductsListView, ProductRetrieveView


urlpatterns = [
    path("products_list/", ProductsListView.as_view(), name="products-list"),
    path("product_detail/<slug:slug>", ProductRetrieveView.as_view(), name="product-detail"),
]
