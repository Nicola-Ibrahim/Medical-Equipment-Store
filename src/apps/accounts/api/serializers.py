from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import ValidationError

from .. import models, profiles
from . import exceptions, tokens


class WarehouseProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles.WarehouseProfile
        fields = [
            "name",
            "working_hours",
            "profit_percentage",
            "warehouse",
        ]

        extra_kwargs = {
            "warehouse": {"write_only": True},
        }


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles.DoctorProfile
        fields = ["first_name", "last_name", "doctor"]

        extra_kwargs = {
            "doctor": {"write_only": True},
        }


class DeliveryWorkerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = profiles.DeliveryWorkerProfile
        fields = "__all__"

        extra_kwargs = {
            "delivery_worker": {"write_only": True},
        }


class UserSerializer(serializers.ModelSerializer):
    """Serializer is responsible for creation and updating an instance"""

    manager_name = serializers.ReadOnlyField(source="manager.admin_profile.first_name")

    groups = serializers.ReadOnlyField(source="groups.all.values")

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    # url = serializers.HyperlinkedIdentityField(
    #     view_name="accounts:details", read_only=True
    # )

    class Meta:
        model = get_user_model()
        ordering = ["-id"]
        profile_related_name = ""
        profile_relation_field = ""
        profile_serializer = None

        fields = [
            "id",
            "email",
            "password",
            "confirm_password",
            "phone_number",
            "state",
            "city",
            "street",
            "zipcode",
            "identification",
            "type",
            "manager_name",
            "is_staff",
            "is_active",
            "is_verified",
            "groups",
            "manager",
        ]

        read_only_fields = ("is_active", "is_staff")
        extra_kwargs = {
            "manager": {"write_only": True},
            "password": {"write_only": True},
            "confirm_password": {"write_only": True},
        }

    def validate(self, attrs):
        """Override validate method to ensure user entered the same password values

        Args:
            attrs (list): the user data

        Raises:
            serializers.ValidationError: raise an error when the two inserted passwords are not similar

        Returns:
            user data: the user data after validation
        """
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def update(self, instance, validated_data):
        # Get user profile data
        profile_data = validated_data.pop("profile")

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

    def create(self, validated_data: dict[str, str]) -> User:
        """Override the create method create a new user with the profile data

        Args:
            validated_data (dict[str, str]): validated data by the serializer

        Returns:
            User: a new inserted user
        """

        # Get the profile data of the user
        user_profile_data = validated_data.pop(self.Meta.profile_related_name)

        # Remove confirm_password field value from the inserted data
        validated_data.pop("confirm_password")

        # Create a new warehouse user without saving
        user = super().create(validated_data)

        # Create profile data for the user
        user_profile_data[self.Meta.profile_relation_field] = user.id
        profile_serializer = self.Meta.profile_serializer(data=user_profile_data)
        profile_serializer.is_valid(raise_exception=True)

        # Save the user's profile
        profile_serializer.save()

        # Save the user
        user.save()

        return user


class WarehouseUserSerializer(UserSerializer):
    """
    A subclass of UserSerializer for handling warehouse users
    """

    profile = WarehouseProfileSerializer(source="warehouse_profile")

    class Meta(UserSerializer.Meta):
        model = models.Warehouse
        fields = UserSerializer.Meta.fields + ["profile"]
        profile_related_name = "warehouse_profile"
        profile_relation_field = "warehouse"
        profile_serializer = WarehouseProfileSerializer


class DoctorUserSerializer(UserSerializer):
    profile = DoctorProfileSerializer(source="doctor_profile")

    class Meta(UserSerializer.Meta):
        model = models.Doctor
        fields = UserSerializer.Meta.fields + ["profile"]
        profile_related_name = "doctor_profile"
        profile_relation_field = "doctor"
        profile_serializer = DoctorProfileSerializer


class DeliveryWorkerUserSerializer(UserSerializer):
    profile = DeliveryWorkerProfileSerializer(source="delivery_worker_profile")

    class Meta(UserSerializer.Meta):
        model = models.DeliveryWorker
        fields = UserSerializer.Meta.fields + ["profile"]
        profile_related_name = "delivery_worker_profile"
        profile_relation_field = "delivery_worker"
        profile_serializer = DeliveryWorkerProfileSerializer


class BaseSerializer(serializers.Serializer):
    """Inherited class from the base Serializer class"""

    def is_valid(self, *, raise_exception=False):
        """Override is_valid method to raise custom exceptions"""

        assert hasattr(self, "initial_data"), (
            "Cannot call `.is_valid()` as no `data=` keyword argument was "
            "passed when instantiating the serializer instance."
        )

        if not hasattr(self, "_validated_data"):
            try:
                self._validated_data = self.run_validation(self.initial_data)
            except ValidationError as exc:
                self._validated_data = {}
                self._errors = exc.detail
            else:
                self._errors = {}

        # Raise Field Error exception
        if self._errors and raise_exception:
            raise exceptions.SerializerFieldsError(errors=self.errors)

        return not bool(self._errors)


class LogoutSerializer(BaseSerializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs.get("refresh")

        return attrs

    def create(self, validated_data):
        tokens.CustomRefreshToken(validated_data.get("refresh"), verify=True).blacklist()
        return True


class ForgetPasswordRequestSerializer(BaseSerializer):
    """This serializer is responsible for creating a number for the user who requested password reset"""

    email = serializers.EmailField(min_length=2, required=True)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email", "")

        # Check the user existence
        user = get_user_model().objects.filter(email=email)

        if not user.exists():
            raise exceptions.UserNotExistsError()

        user = user.first()

        attrs["email"] = email
        attrs["otp"] = models.OTPNumber.get_number()
        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        """Create an OTP number for the user"""

        instance = models.OTPNumber.objects.update_or_create(
            defaults={
                "number": validated_data.get("otp"),
                "user": validated_data.get("user"),
            }
        )
        return instance


class VerifyOTPNumberSerializer(BaseSerializer):
    otp = serializers.CharField(min_length=1, write_only=True)

    def validate(self, attrs):
        otp = attrs.get("otp", "")

        user = self.context["request"].user

        # Check if the OTP number does not exists
        if not models.OTPNumber.objects.filter(user=user).exists():
            raise exceptions.OTPNotExistsError()

        # If the OTP number is expired
        if not models.OTPNumber.objects.get(user=user).check_num(otp):
            raise exceptions.OTPExpiredError()

        return attrs

    def create(self, validated_data):
        """Update the is_verified field after validate the otp number assigned to user"""

        # Get the OTP number of the user
        instance = models.OTPNumber.objects.get(
            user=self.context["request"].user, number=validated_data.get("otp")
        )

        # Set OTP number to be verified
        instance.is_verified = True
        instance.save()

        return True


class ChangePasswordSerializer(BaseSerializer):
    """This serializer is responsible for setting a new password of the user"""

    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirmed_password = serializers.CharField(max_length=128, write_only=True, required=True)
    otp = serializers.CharField(min_length=1, write_only=True, required=True)

    def validate(self, attrs: dict):
        """Validate the inserted data, passwords and otp number"""

        otp = attrs.get("otp", "")

        otp_instance = models.OTPNumber.objects.filter(
            user=self.context["request"].user, number=otp
        )
        if not otp_instance.exists():
            raise exceptions.OTPNotExistsError()

        # Check if the user OTP number is verified
        if not otp_instance[0].is_verified:
            raise exceptions.OTPVerifiedError()

        # Check if the two inserted password are similar
        if attrs["new_password"] != attrs["confirmed_password"]:
            raise exceptions.NotSimilarPasswords()

        # Validate the password if it meets all validator requirements
        password_validation.validate_password(attrs["new_password"], self.context["request"].user)

        return attrs

    def create(self, validated_data):
        """Update the user's password"""

        # Get user from the request
        user = self.context["request"].user

        # Set the new password for the user
        password = validated_data.get("new_password")
        user.set_password(password)

        # Delete otp number for the user
        models.OTPNumber.objects.filter(user=user).delete()

        user.save()

        return user


class FirstTimePasswordSerializer(BaseSerializer):
    """This serializer is responsible for setting a first time password of the user"""

    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirmed_password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate(self, attrs: dict):
        """Validate the inserted data, validate passwords and otp number"""

        # Get the access token from request's header
        request = self.context["request"]
        if not request.headers.get("Authorization"):
            raise exceptions.JWTTokenNotExistsError()

        access_token = request.headers.get("Authorization")
        token_type, access_token = access_token.split(" ")

        # Get the user from access token
        user_id = tokens.CustomAccessToken(access_token, verify=True)["user_id"]
        user = get_user_model().objects.get(pk=user_id)

        # Check if the two inserted password are similar
        if attrs["new_password"] != attrs["confirmed_password"]:
            raise exceptions.NotSimilarPasswords()

        # Validate the password if it meets all validator requirements
        password_validation.validate_password(attrs["new_password"], self.context["request"].user)

        # Add the user instance to validated data
        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        """Update the user's password"""
        user = validated_data.get("user")
        password = validated_data.get("new_password")
        user.set_password(password)

        # Set password changed to true
        if not user.profile.is_password_changed:
            user.profile.is_password_changed = True
            user.profile.save()

        user.save()
        return user
