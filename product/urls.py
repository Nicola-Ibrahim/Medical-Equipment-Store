
from django.urls import path
from .views import (
    ProductsListView,
    ProductDetailsView, 
    ProductsSoldListView,
    )


app_name = 'product'

urlpatterns = [
    path("list/", ProductsListView.as_view(), name="list"),
    path("details/<slug:slug>", ProductDetailsView.as_view(), name="details"),
    path("sold_list/", ProductsSoldListView.as_view(), name="sold-list"),
   
]
