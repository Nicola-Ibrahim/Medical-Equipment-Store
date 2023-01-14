from django.urls import path

from .views import (
    UserDetailsView,
    UserLoginView,
    UserSignView,
    UsersListView,
    VerifyEmail,
)

app_name = "accounts"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("verify_email/", VerifyEmail.as_view(), name="email-verify"),
    path("list/", UsersListView.as_view(), name="list"),
    path("details/", UserDetailsView.as_view(), name="details"),
    path("signup/", UserSignView.as_view(), name="signup"),
]
