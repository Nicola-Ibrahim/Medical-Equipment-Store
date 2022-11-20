
from django.urls import path
from .views import (
    UserDetailsView,
    UserSignUpView,
    UserLoginView,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = 'accounts'

urlpatterns = [
    # path("warehouses_list/", WarehouseListView.as_view(), name="warehouses-list"),
    # path("warehouse_details/<int:pk>/", WarehouseRetrieveView.as_view(), name="warehouse-details"),

    path("get_details/", UserDetailsView.as_view(), name='get-details'),
    path('signup/',UserSignUpView.as_view()),
    path('login/', UserLoginView.as_view()),

    # path('login/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    # path('login/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
