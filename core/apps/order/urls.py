from django.urls import path

from .views import OrderDetailsView, OrdersListView

app_name = "order"

urlpatterns = [
    path("list/", OrdersListView.as_view(), name="list"),
    path("details/<int:pk>/", OrderDetailsView.as_view(), name="details"),
]
