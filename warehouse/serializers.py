from .models import Product
from doctor.models import Order

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
    """
    This serializer only used to update order flags:
    [accepted, submitted, delivered]

    """

    url = serializers.HyperlinkedIdentityField(
        view_name='warehouse:order-update',
        lookup_field='pk',
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            'id', 
            'url',
            'price',
            'status',
            'accepted',
            'submitted',
            'delivered',
            'items',
            # 'related_customer_orders', 
            
        ]
        read_only_fields = ['price', 'status']
        write_only_fields = ['accepted', 'submitted', 'delivered']  
