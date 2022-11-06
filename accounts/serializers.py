from .models import Warehouse
from .profiles import WarehouseProfile
from rest_framework import serializers



class WarehouseProfileSerializer(serializers.ModelSerializer):

    # Reverse M2M relation
    # owner = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = WarehouseProfile
        fields = '__all__'
        excluded_fields = ['id',]

class WarehouseSerializer(serializers.ModelSerializer):

    # Reverse M2M relation
    details = WarehouseProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Warehouse
        fields = [
            'id',
            'details',
            'email',
        ]
        
