
from rest_framework import serializers
from .models import Order, OrderProduct
# from production.models import Product
# from accounts.models import Customer, Staff
# from accounts.serializers import CustomersSerializer, StaffSerializer
# from django.db.models import Q


class OrdersInlineSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    total_price = serializers.IntegerField()




class OrderProductsSerializer(serializers.ModelSerializer):

    product_name = serializers.ReadOnlyField(source='product.name')
    warehouse_name = serializers.ReadOnlyField(source='product.warehouse.first_name')
    class Meta:
        model = OrderProduct
        # fields = [
        #     'price',
        #     'quantity',
        #     'product_name',
        #     'warehouse_name',
        # ]
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):

    # Add extra read_only field
    url = serializers.HyperlinkedIdentityField(
        view_name='order-detail',
        lookup_field='pk',
        read_only=True
    )

    # related_customer_orders = OrdersInlineSerializer(source='customer.customer_orders.all', many=True, read_only=True)

    # M2M relation field
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 
            'url', 
            'price',
            'status',
            'items',
            # 'related_customer_orders', 


            # Write only fields
            'doctor',
            
        ]
        read_only_fields = ['id']
        write_only_fields = ['doctor']

    
    def get_items(self, obj):
        """Custom Method-field to display related items in a specific shape"""
        print(obj)
        # Retrieve the sold items that relate to order 
        qs = OrderProduct.objects.filter(order=obj)
        return OrderProductsSerializer(qs, many=True, context=self.context).data

    # def to_internal_value(self, data):
    #     """Change the inserting data from str to num for model"""

        
    #     data['customer'] = Customer.objects.get(username=data.get('customer'))
    #     data['staff'] = Staff.objects.get(username=data.get('staff'))
      

    #     for item in data.get('items'):
    #         if(isinstance(item['item'], str)):
    #             item['item'] = Product.objects.get(name=item['item']).id
        
    #     return data


    # def create(self, validated_data):
    #     order_items: list = validated_data.pop('items')

    #     # Check available items
    #     for order_item in order_items:
    #         item = Product.objects.get(id=order_item['item'])
    #         item.is_available(order_item['consume_quantity'])

    #     # Create order instance
    #     instance = super().create(validated_data)

    #     for item in order_items:
    #         item['order'] = instance.id
        
    #     # Link order with inserted items
    #     ser = OrderProductsSerializer(data=order_items, many=True)
    #     ser.is_valid(raise_exception=True)
    #     ser.save()


    #     return instance


    
