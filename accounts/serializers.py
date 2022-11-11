from .models import Warehouse
from .profiles import WarehouseProfile
from rest_framework import serializers

class PermissionGroupsInlineSerializer(serializers.Serializer):
    name = serializers.CharField()



class WarehouseProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = WarehouseProfile
        fields = '__all__'

        extra_kwargs = {
            'warehouse': {'write_only': True},
        }

class WarehouseSerializer(serializers.ModelSerializer):
    
    url = serializers.HyperlinkedIdentityField(
        view_name='accounts:warehouse-details',
        lookup_field='pk',
        read_only=True
    )

    manager_name = serializers.ReadOnlyField(source='manager.admin_profile.first_name')

    groups = PermissionGroupsInlineSerializer(source='groups.all', many=True, read_only=True)

    # Reverse relation
    profile = WarehouseProfileSerializer(source='warehouse_profile')

    class Meta:
        model = Warehouse
        fields = [
            'id',
            'url',
            'profile',
            'email',
            'password',
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
            'password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        # Get warehouse user profile data
        profile_data = validated_data.pop('warehouse_profile')

        # Update main data of the warehouse user
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

    def create(self, validated_data):
        # Get warehouse user profile data
        profile_data = validated_data.pop('warehouse_profile')

        # Create a new warehouse user
        instance = super().create(validated_data)

        # Create profile data for the user
        profile_data['warehouse'] = instance.id

        profile = WarehouseProfileSerializer(data=profile_data)
        profile.is_valid(raise_exception=True)
        profile.save()

        return instance