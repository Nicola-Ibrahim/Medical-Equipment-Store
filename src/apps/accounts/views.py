import jwt
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from src.apps.accounts.services import send_verification
from src.home import settings

from .mixins import (
    DeleteUserPermissionMixin,
    FilterMixin,
    InUserTypeQuerySetMixin,
    InUserTypeSerializerMixin,
    KwargUserTypeQuerySetMixin,
    KwargUserTypeSerializerMixin,
    PermissionMixin,
)
from .models import User
from .serializers import UserLoginSerializer, UserSerializer


class UserLoginView(GenericAPIView):
    """Login view"""

    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
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
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"], type=jwt)

            # Get the use id from the payload
            user = User.objects.get(id=payload["user_id"])

            # Check if the user is not verified
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({"email": "Successfully activated"}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Activation Expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.exceptions.DecodeError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


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
    InUserTypeQuerySetMixin,
    InUserTypeSerializerMixin,
    PermissionMixin,
    RetrieveAPIView,
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


class UserUpdateView(
    InUserTypeQuerySetMixin,
    # InUserTypeSerializerMixin,
    PermissionMixin,
    UpdateAPIView,
):
    serializer_class = UserSerializer

    def get_object(self):
        """
        Returns the object the view is displaying.
        """
        queryset = self.filter_queryset(self.get_queryset())

        filter_kwargs = {self.lookup_field: self.request.user.id}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class UserDeleteView(
    InUserTypeQuerySetMixin,
    InUserTypeSerializerMixin,
    DeleteUserPermissionMixin,
    DestroyAPIView,
):
    def get_object(self):
        """
        Returns the object the view is displaying.
        """
        queryset = self.filter_queryset(self.get_queryset())

        filter_kwargs = {self.lookup_field: self.request.user.id}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def destroy(self, request, *args, **kwargs):
        """Override destroy method to handle deleting for multiple users

        Args:
            request: incoming request
        """

        # Get the users to be deleted
        ids = request.data["ids"]

        # Get the user who perform the delete action
        _ = self.get_object()

        # Execute delete the ids
        users_deleted = self.perform_destroy(ids)

        msg = {"details": f"Deleted the users: {users_deleted}"}
        return Response(data=msg, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, ids):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {"pk__in": ids}
        users_deleted = queryset.filter(**filter_kwargs).delete()
        return users_deleted


class UsersListView(
    KwargUserTypeQuerySetMixin,
    KwargUserTypeSerializerMixin,
    FilterMixin,
    PermissionMixin,
    ListAPIView,
):
    pass
