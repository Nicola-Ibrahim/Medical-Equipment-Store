
from rest_framework import serializers
from .models import Order, OrderProduct
from product.models import Product
from core.utils import send_msg
from accounts.models import User

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
        view_name='order:order-details',
        lookup_field='pk',
        read_only=True
    )
    order_id = serializers.ReadOnlyField(source='id')
    doctor_name = serializers.ReadOnlyField(source='doctor.doctor_profile.first_name')

    
    # M2M relation field
    # products = serializers.SerializerMethodField()
    products = OrderProductsSerializer(source='order_set.all', many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'order_id', 
            'url', 
            'doctor_name',
            'price',
            'status',
            'doctor',
            'products',
            
        ]

        read_only_fields = ['id', 'price']
        extra_kwargs = {
            'order': {'write_only': True},
        }
    
    def get_products(self, obj):
        """Custom Method-field to display order related products"""

        # Get products related to order
        qs = obj.order_set.all()
        return OrderProductsSerializer(qs, many=True, context=self.context).data


    def check_product_availability(self, products):
        """Check available products"""

        for product_details in products:
            product = Product.objects.get(name=product_details['name'])

            availability, available_quantity = product.is_available(consume_quantity=product_details['quantity'])
            if(not availability):
                raise serializers.ValidationError(f"You exceed the number of available for the {product.name}:{product.quantity}")

        return True

    def to_internal_value(self, data):
        data = data.copy()
        data['doctor'] = self.context['request'].user
        return data


    def create(self, validated_data):
        products_data: list = validated_data.pop('products')


        self.check_product_availability(products_data)
        instance = super().create(validated_data)

        
        # Link order with inserted products
        self.context['order'] = instance.id
        ser = OrderProductsSerializer(data=products_data, many=True, context=self.context)
        ser.is_valid(raise_exception=True)
        ser.save()


        return instance
    
    def update(self, instance, validated_data):
        user = self.context['request'].user
        
        if(user.type not in (User.Type.ADMIN, User.Type.DOCTOR)):
            # Allow change only the order status
            status = validated_data.get('status')
            validated_data = {'status': status}
            send_msg(status)

        return super().update(instance, validated_data)



