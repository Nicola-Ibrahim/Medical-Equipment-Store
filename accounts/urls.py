
from django.urls import path
from .views import (
    UserDetailsView,
    UserSignView,
    UserLoginView,
    VerifyEmail,
)

app_name = 'accounts'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),

    path("verify_email/", VerifyEmail.as_view(), name='email-verify'),
    path("get_details/", UserDetailsView.as_view(), name='get-details'),
    path('signup/',UserSignView.as_view(), name='signup'),
    

]
