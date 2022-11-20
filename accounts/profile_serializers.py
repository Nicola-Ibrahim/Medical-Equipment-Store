from rest_framework import serializers
from .profiles import WarehouseProfile, DoctorProfile, DeliveryWorkerProfile


class WarehouseProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = WarehouseProfile
        fields = '__all__'

        extra_kwargs = {
            'warehouse': {'write_only': True},
        }

class DoctorProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorProfile
        fields = '__all__'

        extra_kwargs = {
            'doctor': {'write_only': True},
        }

class DeliveryWorkerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryWorkerProfile
        fields = '__all__'

        extra_kwargs = {
            'delivery_worker': {'write_only': True},
        }


