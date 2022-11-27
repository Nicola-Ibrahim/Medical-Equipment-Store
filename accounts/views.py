from rest_framework.generics import (
    GenericAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from django.core.exceptions import ViewDoesNotExist

from home import settings
import jwt

from .serializers import UserLoginSerializer, WarehouseUserSerializer, DoctorUserSerializer, DeliveryWorkerUserSerializer, UserSerializer
from .models import User
from .services import send_verification

class UserLoginView(GenericAPIView):
    """
    Class based view to register a warehouse 
    """
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class VerifyEmail(APIView):
    """verify the mail that send in the mail box"""

    permission_classes = [AllowAny]

    def get(self, request):
        token = request.GET.get('token')
        try:
            # Decode the token coming with the request
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"], type=jwt)

            # Get the use id from the payload
            user = User.objects.get(id=payload['user_id'])

            # Check if the user is not verified 
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class UserSignView(APIView):
    permission_classes = [AllowAny,]
    # renderer_classes = (UserRenderer,)

    def get_serializer_class(self):
        """
        Override method to get serializer_class depending on the url parameters
        """
        serializers_classes = {
            'warehouse': WarehouseUserSerializer,
            'doctor': DoctorUserSerializer,
            'delivery_worker': DeliveryWorkerUserSerializer,
        }
        
        serializers_class = serializers_classes.get(self.request.query_params.get('type'))
        if(not serializers_class):
            return UserSerializer

        return serializers_class


    def post(self, request):
        user_data = request.data
        serializer = self.get_serializer(data=user_data, context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        send_verification(user_data=user_data, request=request)
        return Response(user_data, status=status.HTTP_201_CREATED)


class UserDetailsView(APIView):
    """
    Class based view to Get Warehouse User Details using Token Authentication
    """
    queryset = User.objects.all()

    def get_serializer_class(self):
        """
        Override method to get serializer_class depending on the url parameters
        """
        serializers_classes = {
            'warehouse': WarehouseUserSerializer,
            'doctor' : DoctorUserSerializer,
            'delivery_worker' : DeliveryWorkerUserSerializer,
        }

        # Change the serializer depending on the authenticated user type
        serializers_class = serializers_classes.get(self.request.user.type.lower())
        if(not serializers_class):
            return UserSerializer

        return serializers_class

    def get(self, request, *args, **kwargs):
        user = self.get_queryset().get(id=request.user.id)
        serializer = self.get_serializer(user, context={'request':request})
        return Response(serializer.data)



