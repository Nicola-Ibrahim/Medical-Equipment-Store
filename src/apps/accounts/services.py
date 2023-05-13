import logging
from abc import ABC, abstractmethod
from typing import Any

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class BaseEmailService(ABC):
    """An abstract class for email service"""

    def __init__(self, subject: str, message: str, to: str) -> None:
        self.subject = subject
        self.message = message
        self.to = [to]

    @abstractmethod
    def init_email(self):
        raise Exception("Must implement")

    @abstractmethod
    def send_email(self):
        raise Exception("Must implement")


class GmailService(BaseEmailService):
    """Concrete Gmail service for establishing a Gmail service for sending an email"""

    def __init__(self, subject: str, message: str, from_email: str, to: str) -> None:
        self.mail = EmailMessage()
        self.from_email = from_email
        super().__init__(subject, message, to)

    def init_email(self) -> None:
        self.mail.subject = self.subject
        self.mail.body = self.message
        self.mail.from_email = self.from_email
        self.mail.to = self.to

    def send_email(self) -> None:
        self.init_email()
        self.mail.send(fail_silently=False)


class ConsolEmailService(BaseEmailService):
    """Concrete consol service for displaying an email in consol (For debugging goal)"""

    def __init__(self, subject: str, message: str, to: str) -> None:
        self.logger = logging.getLogger(__name__)
        super().__init__(subject, message, to)

    def init_email(self) -> str:
        message = f"{self.subject}\n{self.message}\n{self.to}"
        return message

    def send_email(self) -> None:
        message = self.init_email()
        self.logger.info(message)


class BaseMailer(ABC):
    """An abstract mailer for sending an email.

    This class provides a common interface and functionality for different
    email services. It uses a factory method to create suitable email services
    depending on the settings. It also defines an abstract method to edit the
    message if additional data should be added.
    """

    def __init__(self, subject: str, message: str, to_email: str) -> None:
        """Initialize the BaseMailer with the given arguments.

        Args:
            subject (str): The subject of the email.
            message (str): The body of the email.
            to_email (str): The recipient of the email.
        """
        self.subject = subject
        self.message = message
        self.to_email = to_email

        self.email_service: BaseEmailService = None

        # Add new changes to email's message if there is any.
        self.edit_message()

        # Create an email services depending on the configuration settings
        self.create_service()

    def create_service(self) -> None:
        """Factory method to create suitable email services depending on the define settings.

        This method assigns the email_service attribute to an instance of a subclass of
        BaseEmailService based on the value of settings.EMAIL_BACKEND. It also calls the
        edit_message method to add any changes to the message.

        Raises:
            ValueError: If settings.EMAIL_BACKEND is not a valid option.
        """

        # Email in Gmail
        if settings.EMAIL_BACKEND == "django.core.mail.backends.smtp.EmailBackend":
            self.email_service = GmailService(
                subject=self.subject,
                message=self.message,
                from_email=settings.EMAIL_HOST_USER,
                to=self.to_email,
            )

        # Email in consol
        elif settings.EMAIL_BACKEND == "django.core.mail.backends.console.EmailBackend":
            self.email_service = ConsolEmailService(
                subject=self.subject, message=self.message, to=self.to_email
            )

    def init_email(self) -> None:
        """Create an email entity with the plugged data.

        This method calls the init_email method of the email_service object to create an
        email entity with the given subject, message and recipient.

        Raises:
            Exception: If email_service is None.
        """
        if not self.email_service:
            raise Exception("You must provide an email service")

        self.email_service.init_email()

    def send_email(self) -> None:
        """Send the email using the email service.

        This method calls the send_email method of the email_service object to send the
        email entity. It also handles any exceptions that may occur during the process and
        logs them using a logger object.

        """
        self.init_email()

        try:
            self.email_service.send_email()

        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error("Error at %s", "mailer", exc_info=e)

    @abstractmethod
    def edit_message(self) -> None:
        """Edit message if addition data should be added.

        This is an abstract method that should be implemented by subclasses of BaseMailer
        to modify the message attribute if necessary. For example, adding a signature or a
        greeting.
        """


class RegisterMailer(BaseMailer):
    """Concrete Mailer for sending a welcome email with password to the user.

    This class inherits from BaseMailer and implements the edit_message method to add the
    user's full name and password to the message.

    """

    def __init__(self, to_email, full_name, password) -> None:
        """Initialize the RegisterMailer with the given arguments.

        Args:
            to_email (str): The recipient of the email.
            full_name (str): The user's full name.
            password (str): The user's password.
        """
        self.full_name = full_name
        self.password = password
        super().__init__(
            subject=settings.EMAIL_REGISTER_SUBJECT,
            message=settings.EMAIL_REGISTER_MESSAGE,
            to_email=to_email,
        )

    def edit_message(self) -> None:
        """Edit message by adding the user's full name and password.

        This method overrides the abstract method of BaseMailer and appends the user's full
        name and password to the message attribute.

        """
        self.message += f"\n{self.full_name}\nYour password is:'{self.password}'"


class OTPMailer(BaseMailer):
    """Concrete Mailer for sending an email with OTP number to the user.

    This class inherits from BaseMailer and implements the edit_message method to add the
    OTP number to the message.

    """

    def __init__(self, to_email: str, otp_number: str) -> None:
        """Initialize the OTPMailer with the given arguments.

        Args:
            to_email (str): The recipient of the email.
            otp_number (str): The OTP number for resetting the password.
        """
        self.otp_number = otp_number
        super().__init__(
            subject=settings.EMAIL_RESETPASSWORD_SUBJECT,
            message=settings.EMAIL_RESETPASSWORD_MESSAGE,
            to_email=to_email,
        )

    def edit_message(self) -> None:
        """Edit message by adding the OTP number.

        This method overrides the abstract method of BaseMailer and appends the OTP number
        to the message attribute.

        """
        self.message += f"\n otp:'{self.otp_number}'"


class VerificationMailer(BaseMailer):
    """Concrete Mailer for sending a verification email to the new registered user with token value.

    This class inherits from BaseMailer and implements the edit_message method to add a link
    with a token value for verifying the user's email.

    """

    def __init__(self, to_email: str, token: str, request) -> None:
        """Initialize the VerificationMailer with the given arguments.

        Args:
            to_email (str): The recipient of the email.
            token (str): The token value for verifying the email.
            request (HttpRequest): The request object that contains information about the current site domain.
        """
        self.to_email = to_email
        self.token = token
        self.request = request

        super().__init__(
            subject=settings.EMAIL_EMAIL_VERIFICATION_SUBJECT,
            message=settings.EMAIL_EMAIL_VERIFICATION_MESSAGE,
            to_email=to_email,
        )

    def edit_message(self) -> None:
        """Edit message by adding a link with a token value for verifying the email.

        This method overrides the abstract method of BaseMailer and appends a link with a token value
        for verifying the email to the message attribute. It uses some helper functions and models to
        construct the link.

        """
        # Get the user by the inserted email
        user = User.objects.get(email=self.to_email)

        # Get refresh token to this user
        token = RefreshToken.for_user(user).access_token

        # Get the current site domain
        current_site = get_current_site(self.request).domain

        # Get the url of the "email-verify" view
        relativeLink = reverse("accounts:email-verify")  # -> /api/accounts/verify_email/

        # Sum up the final url for verification
        absurl = "http://" + current_site + relativeLink + "?token=" + str(token)

        self.message += f"Hi {user.email} Use the link below to verify your email\n{absurl}"
