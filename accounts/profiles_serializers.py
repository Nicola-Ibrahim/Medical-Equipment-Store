from rest_framework import serializers

from .profiles import (DeliveryWorkerProfile, DoctorProfile, Section, Service,
                       WarehouseProfile)


class SectionSerializer(serializers.ModelSerializer):

    warehouse_name = serializers.ReadOnlyField(source='warehouse.name')

    class Meta:
        model = Section
        fields = ['name', 'warehouse_name']


class ServiceSerializer(serializers.ModelSerializer):

    warehouse_name = serializers.ReadOnlyField(source='warehouse.name')

    class Meta:
        model = Service
        fields = ['name', 'warehouse_name']


class WarehouseProfileSerializer(serializers.ModelSerializer):

    sections = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Section.objects.all()
    )
    services = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Service.objects.all()
    )

    class Meta:
        model = WarehouseProfile
        fields = ['name', 'sections', 'services',
                  'working_hours', 'profit_percentage', 'warehouse']

        extra_kwargs = {
            'warehouse': {'write_only': True},
        }
        validators = []

    def validate_sections(self, values: list):
        """Validate inserted sections values

        Args:
            values (list): list of sections
        """
        def get_id(value: int | str | Section):
            """Get section id

            Args:
                value (int | str | Section): section value

            Returns:
                id (int): The returned id of a section
            """
            match value:
                case int():
                    return value

                case Section():
                    id = Section.objects.get(name=value).pk

                case str():
                    id = Section.objects.get(name=value).pk

            return id

        id_values = list(map(get_id, values))
        return id_values

    def validate_services(self, values: list):
        """Validate inserted services values

        Args:
            values (list): list of services
        """
        def get_id(instance: int | str | Service):
            """Get service id

            Args:
                value (int | str | Section): service value

            Returns:
                id: The returned id of a service
            """
            match instance:
                case int():
                    return id
                case Service():
                    id = Service.objects.get(name=instance).pk

                case str():
                    id = Service.objects.get(name=instance).pk

            return id

        id_values = list(map(get_id, values))
        return id_values


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
