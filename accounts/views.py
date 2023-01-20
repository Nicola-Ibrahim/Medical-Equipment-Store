import jwt
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

from core.services import send_verification
from home import settings

from .mixins import (
    FilterMixin,
    KwargUserTypeQuerySetMixin,
    KwargUserTypeSerializerMixin,
    PermissionMixin,
    UserTypeQuerySetMixin,
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

    permission_classes = (AllowAny,)

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


class UserSignView(KwargUserTypeSerializerMixin, CreateAPIView):
    """View for adding a new user"""

    permission_classes = (AllowAny,)

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


class UserDetailsView(
    UserTypeQuerySetMixin,
    UserTypeSerializerMixin,
    PermissionMixin,
    RetrieveUpdateDestroyAPIView,
):
    """
    Class based view to Get Warehouse User Details using Token Authentication
    """

    def get(self, request, *args, **kwargs) -> Response:
        """Override get method to obtain details depending on login user type

        Args:
            request: incoming request

        Returns:
            Response: rest framework response with user data
        """

        serializer = self.get_serializer(request.user, context={"request": request})
        return Response(serializer.data)

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        print("-" * 40)
        print(self.lookup_url_kwarg)
        print("-" * 40)

        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class UsersListView(
    KwargUserTypeQuerySetMixin,
    KwargUserTypeSerializerMixin,
    FilterMixin,
    PermissionMixin,
    ListAPIView,
):
    pass
