from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import exceptions, serializers

from .models import DeliveryWorker, Doctor, User, Warehouse
from .profiles_serializers import (DeliveryWorkerProfileSerializer,
                                   DoctorProfileSerializer,
                                   WarehouseProfileSerializer)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer is responsible for creation and updating an instance
    """
    
    manager_name = serializers.ReadOnlyField(source='manager.admin_profile.first_name')

    groups = serializers.ReadOnlyField(source="groups.all.values")

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)


    # Reverse relation

    class Meta:
        model = User
        ordering = ['-id']
        profile_related_name = ''
        profile_relation_field = ''

        fields = [
            'id',
            'email',
            'password',
            'confirm_password',
            'phone_number',
            'state',
            'city',
            'street', 
            'zipcode',
            'identification', 
            'type',
            'manager_name',
            'is_staff',
            'is_active',
            'groups',


            'manager',
        ]

        read_only_fields = ('is_active', 'is_staff')
        extra_kwargs = {
            'manager': {'write_only': True},
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }

    def validate(self, attrs):
        if(attrs['password'] != attrs['confirm_password']):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def update(self, instance, validated_data):

        # Get user profile data
        profile_data = validated_data.pop('profile')

        # Update main data of the user
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update profile data of the user
        profile = instance.warehouse_profile
        for attr, value in profile_data.items():
            setattr(profile, attr, value)

        # Save instance
        profile.save()
        instance.save()

        return instance

    def create(self, validated_data:dict):

        # Get warehouse user profile data
        user_profile_data = validated_data.pop(self.Meta.profile_related_name)

        # Remove confirm_password field value from inserting data
        validated_data.pop('confirm_password')

        # Create a new warehouse user
        user = super().create(validated_data)

        # Create profile data for the user
        user_profile_data[self.Meta.profile_relation_field] = user.id

        profile_serializer = self.get_profile_serializer()
        profile_serializer = profile_serializer(data=user_profile_data)
        profile_serializer.is_valid(raise_exception=True)


        #TODO: Check the validity of profile data before create a user 

        profile_serializer.save()

        return user

    def get_profile_serializer(self):
        dic = {
            'warehouse_profile': WarehouseProfileSerializer,
            'doctor_profile': DoctorProfileSerializer,
            'delivery_worker_profile': DeliveryWorkerProfileSerializer,
        }

        return dic.get(self.Meta.profile_related_name)

class UserLoginSerializer(serializers.Serializer):

    """
    A serializer for handling the login process for a user
    """
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=128,
        write_only=True
    )

    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'type',
            'tokens',
        ]

    def get_tokens(self, obj):
        user = self.Meta.model.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')


        if email and password:
            user = authenticate(request=self.context['request'],
                                username=email, password=password)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')

            if not user.is_active:
                raise serializers.ValidationError('Account disabled, contact admin')

            if not user.is_verified:
                raise serializers.ValidationError('Email is not verified')

        attrs['email'] = user.email
        attrs['tokens'] = user.tokens()
        return super().validate(attrs)


class WarehouseUserSerializer(UserSerializer):

    """
    A subclass of UserSerializer for handling warehouse users
    """

    # url = serializers.HyperlinkedIdentityField(
    #     view_name='accounts:get-details',
    #     lookup_field='pk',
    #     read_only=True
    # )

    profile = WarehouseProfileSerializer(source='warehouse_profile')

    class Meta(UserSerializer.Meta):
        model = Warehouse
        fields = UserSerializer.Meta.fields + ['profile']
        profile_related_name = 'warehouse_profile'
        profile_relation_field = 'warehouse'


class DoctorUserSerializer(UserSerializer):

    # url = serializers.HyperlinkedIdentityField(
    #     view_name='accounts:get-details',
    #     lookup_field='pk',
    #     read_only=True
    # )

    profile = DoctorProfileSerializer(source='doctor_profile')

    class Meta(UserSerializer.Meta):
        model = Doctor
        fields = UserSerializer.Meta.fields + ['profile']
        profile_related_name = 'doctor_profile'
        profile_relation_field = 'doctor'


class DeliveryWorkerUserSerializer(UserSerializer):

    # url = serializers.HyperlinkedIdentityField(
    #     view_name='accounts:get-details',
    #     lookup_field='pk',
    #     read_only=True
    # )

    profile = DeliveryWorkerProfileSerializer(source='delivery_worker_profile')

    class Meta(UserSerializer.Meta):
        model = DeliveryWorker
        fields = UserSerializer.Meta.fields + ['profile']
        profile_related_name = 'delivery_worker_profile'
        profile_relation_field = 'delivery_worker'
