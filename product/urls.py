
from django.urls import path
from .views import (
    ProductsListView,
    ProductDetailsView, 
    ProductsSoldListView,
    )


app_name = 'product'

urlpatterns = [
    path("products_list/", ProductsListView.as_view(), name="products-list"),
    path("product_details/<slug:slug>", ProductDetailsView.as_view(), name="product-details"),
    path("products_sold_list/", ProductsSoldListView.as_view(), name="product-sold-list"),
   
]
