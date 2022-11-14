from .models import Product
from doctor.models import Order, OrderProduct
from doctor.serializers import OrderProductsSerializer

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
            'slug',
            'created_at',
            'updated_at',
            'warehouse'
        ]
        read_only_fields = ['url', 'slug', 'created_at', 'updated_at']
        write_only_fields = ['id','warehouse']


    def to_internal_value(self, data):
        """Change data attributes value"""
        
        # data._mutable = True  # make data to be immutable
        print(data)
        
        # Connect the warehouse to current user
        data['warehouse'] = self.context['request'].user.id
        
        # data._mutable = False  # make data to be mutable
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
        read_only_fields = ['price', 'status']

    def get_items(self, obj):
        """Custom Method-field to display related items in a specific shape"""
        # Retrieve the sold items that relate to order 
        qs = OrderProduct.objects.filter(order=obj)
        return OrderProductsSerializer(qs, many=True, context=self.context).data