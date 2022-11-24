
from rest_framework import serializers
from .models import Order, OrderProduct
from product.models import Product

class OrdersInlineSerializer(serializers.Serializer):
    """
    READ ONLY serializer for displaying related orders for a product  
    """
    id = serializers.IntegerField()
    total_price = serializers.IntegerField()


class OrderProductsSerializer(serializers.ModelSerializer):

    product_name = serializers.ReadOnlyField(source='product.name')
    warehouse_name = serializers.ReadOnlyField(source='product.warehouse.warehouse_profile.name')
    
    class Meta:
        model = OrderProduct
        fields = [
            'product_name',
            'warehouse_name',
            'quantity',
            'discount',
            'price',
            'order',
            'product',
        ]

        extra_kwargs = {
            'order': {'write_only': True},
            'product': {'write_only': True},
            'price': {'read_only': True},
        }

    def to_internal_value(self, data):
        """
        Override method to add more necessary data 
        """

        # Add product field to the data 
        data['product'] = Product.objects.get(name=data['name']).id
        data['order'] = self.context['order']
        return super().to_internal_value(data)
    

class OrderSerializer(serializers.ModelSerializer):

    """
    It handles displaying and inserting of a new order with its products 
    """

    # Add extra read_only field
    url = serializers.HyperlinkedIdentityField(
        view_name='doctor:order-details',
        lookup_field='pk',
        read_only=True
    )

    doctor_name = serializers.ReadOnlyField(source='doctor.doctor_profile.first_name')

    
    # M2M relation field
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 
            'url', 
            'doctor_name',
            'price',
            'status',
            'accepted',
            'submitted',
            'delivered',
            'items',
            'doctor',
            
        ]

        read_only_fields = ['id', 'status', 'price', 'accepted', 'submitted', 'delivered']
        extra_kwargs = {
            'doctor': {'write_only': True},
        }
    
    def get_items(self, obj):
        """Custom Method-field to display order related items"""
        qs = OrderProduct.objects.filter(order=obj)
        return OrderProductsSerializer(qs, many=True, context=self.context).data

    def to_internal_value(self, data):
        data['doctor'] = self.context['request'].user
        return data

    def create(self, validated_data):
        items: list = validated_data.pop('items')

        # TODO: Apply item availability before inserting 

        # Check available items
        for item_details in items:
            item = Product.objects.get(name=item_details['name'])

            availability, available_quantity = item.is_available(consume_quantity=item_details['quantity'])
            if(not availability):
                raise serializers.ValidationError(f"You exceed the number of available for the {item.name}:{item.quantity}")


        
        # Create a new order
        instance = super().create(validated_data)

        # add
        self.context['order'] = instance.id
        
        # Link order with inserted items
        ser = OrderProductsSerializer(data=items, many=True, context=self.context)
        ser.is_valid(raise_exception=True)
        ser.save()


        return instance


    
