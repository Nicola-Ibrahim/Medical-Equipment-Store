import jwt
from core.services import send_verification
from home import settings
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .mixins import (
    FilterMixin,
    QuerySetMixin,
    SerializerParamsMixin,
    UserTypeSerializerMixin,
)
from .models import User
from .serializers import UserLoginSerializer


class UserLoginView(GenericAPIView):
    """Login view"""

    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyEmail(APIView):
    """Verify the user by the token send it to the email"""

    permission_classes = [AllowAny]

    def get(self, request) -> Response:
        """Override get method to verify the new registered user via email

        Args:
            request: the incoming request

        Raises:
            jwt.ExpiredSignatureError | jwt.exceptions.DecodeError: jwt exceptions

        Returns:
            Response | Exception: rest framework response with verified message or exception
        """

        token = request.GET.get("token")
        try:
            # Decode the token coming with the request
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"], type=jwt
            )

            # Get the use id from the payload
            user = User.objects.get(id=payload["user_id"])

            # Check if the user is not verified
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response(
                {"email": "Successfully activated"}, status=status.HTTP_200_OK
            )

        except jwt.ExpiredSignatureError as identifier:
            return Response(
                {"error": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError as identifier:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class UserSignView(SerializerParamsMixin, CreateAPIView):
    """View for adding a new user"""

    permission_classes = [
        AllowAny,
    ]
    # renderer_classes = (UserRenderer,)

    def post(self, request, *args, **kwargs) -> Response:
        """Override post method to control the behavior of inserting a new user

        Returns:
            Response: rest framework response with user data
        """
        user_data = request.data
        serializer = self.get_serializer(data=user_data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        
        # Send verification message to user's email
        send_verification(user_data=user_data, request=request)

        return Response(user_data, status=status.HTTP_201_CREATED)


class UserDetailsView(UserTypeSerializerMixin, RetrieveUpdateDestroyAPIView):
    """
    Class based view to Get Warehouse User Details using Token Authentication
    """

    queryset = User.objects.all()

    def get(self, request, *args, **kwargs) -> Response:
        """Override get method to obtain details depending on login user type

        Args:
            request: incoming request

        Returns:
            Response: rest framework response with user data
        """
        user = self.get_queryset().get(id=request.user.id)
        serializer = self.get_serializer(user, context={"request": request})
        return Response(serializer.data)


class UsersListView(QuerySetMixin, UserTypeSerializerMixin, FilterMixin, ListAPIView):
    pass
