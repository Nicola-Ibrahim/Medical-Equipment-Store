from rest_framework import serializers
from .profiles import WarehouseProfile, DoctorProfile, DeliveryWorkerProfile, Section, Service

class SectionSerializer(serializers.ModelSerializer):

    # warehouses = WarehouseProfileSerializer(many=True, read_only=True)
    
    class Meta:
        model = Section
        fields = ['name',]

class ServiceSerializer(serializers.ModelSerializer):

    # warehouses = WarehouseProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = ['name',]

class WarehouseProfileSerializer(serializers.ModelSerializer):

    # sections = SectionSerializer(many=True)
    # services = ServiceSerializer(many=True)

    class Meta:
        model = WarehouseProfile
        fields = ['name', 'sections', 'services', 'working_hours', 'profit_percentage', 'warehouse']

        # extra_kwargs = {
        #     'warehouse': {'write_only': True},
        # }

    # def to_internal_value(self, data):
    #     # print(data.getlist('sections')[:])
    #     # print(data.getlist('services')[:])

    #     # MultiValueDict

    #     # print('-'*50)
    #     data["sections"] = Section.objects.filter(id__in=data['sections']).values_list('id', flat=True)
    #     data["services"] = Service.objects.filter(id__in=data['services']).values_list('id', flat=True)

    #     print('to internal:', data)
    #     print('to internal sections',data['sections'])
    #     return super().to_internal_value(data)








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


