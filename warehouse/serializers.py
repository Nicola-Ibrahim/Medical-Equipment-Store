from .models import Product
from doctor.models import OrderProduct

from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field = 'slug',
        read_only=True,
    )

    # Reverse M2M relation
    # orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 
            'url', 
            'name', 
            'price',
            'quantity',
            'slug',
            'created',
            'updated',
            'warehouse'
        ]
        read_only_fields = ['url', 'slug', 'created', 'updated']
        write_only_fields = ['id','warehouse']


    def to_internal_value(self, data):
        """Change data attributes value"""
        
        data._mutable = True  # make data to be immutable

        # Connect the warehouse to current user
        data['warehouse'] = str(self.context['request'].user.id)

        data._mutable = False  # make data to be mutable
        return super().to_internal_value(data)



class WarehouseOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'
    