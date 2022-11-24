from .models import Product
from .services import send_msg
from order.models import Order, OrderProduct
from order.serializers import OrderProductsSerializer
from accounts.models import Warehouse

from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='warehouse:product-details',
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
            'visible',
            'slug',
            'created_at',
            'updated_at',
            'warehouse'
        ]
        read_only_fields = ['url', 'slug', 'created_at', 'updated_at']


    def to_internal_value(self, data):
        """Change data attributes value"""

        # Connect the warehouse to current user
        data['warehouse'] = self.context['request'].user.id
        
        return super().to_internal_value(data)



class WarehouseOrdersSerializer(serializers.ModelSerializer):
    """
    This serializer only used to update order flags:
    [accepted, submitted, delivered, rejected]

    """

    url = serializers.HyperlinkedIdentityField(
        view_name='warehouse:order-update',
        lookup_field='pk',
        read_only=True
    )

    items = serializers.SerializerMethodField()

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
            'rejected',
            'items',
            
        ]
        read_only_fields = ['id', 'url', 'price', 'status']

    def get_items(self, obj):
        """Custom Method-field to display related items in a specific shape"""
        # Retrieve the sold items that relate to order 
        qs = OrderProduct.objects.filter(order=obj)
        return OrderProductsSerializer(qs, many=True, context=self.context).data

    def update(self, instance, validated_data):
        if(validated_data.get('accepted')):
            send_msg('accepted')
        return super().update(instance, validated_data)

class ProductsSoldSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    sold_count = serializers.IntegerField(read_only=True)

    warehouse_name = serializers.SerializerMethodField()
    
    def get_warehouse_name(self, obj):
        qs = Warehouse.objects.get(id=obj['warehouse'])
        name = qs.warehouse_profile.name
        return name