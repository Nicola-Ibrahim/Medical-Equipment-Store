from django.contrib.sites.shortcuts import get_current_site
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from core.apps.accounts.models import User


def send_verification(user_data: dict[str, str], request) -> None:
    """Send a verification email to the new registered user with token value.

    Args:
        user_data (dict[str, str]): the new user data
        request: incoming request

    """

    # Get the user by the inserted email
    user = User.objects.get(email=user_data["email"])

    # Get refresh token to this user
    token = RefreshToken.for_user(user).access_token

    # Get the current site domain
    current_site = get_current_site(request).domain

    # Get the url of the "email-verify" view
    relativeLink = reverse("accounts:email-verify")  # -> /api/accounts/verify_email/

    # Sum up the final url for verification
    absurl = "http://" + current_site + relativeLink + "?token=" + str(token)

    email_body = (f"Hi {user.email} Use the link below to verify your email\n{absurl}")

    verification_data = {
        "email_body": email_body,
        "to_email": user.email,
        "email_subject": "Verify your email",
    }

    send_email(verification_data)


def send_email(data: dict[str, str]) -> None:
    """Send verification token to the new user

    Args:
        data (dict): data contains email to be send to and verification token
    """

    print(data)
