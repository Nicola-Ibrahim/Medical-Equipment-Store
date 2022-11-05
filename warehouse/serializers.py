from .models import Product
from rest_framework import serializers



class ProductSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field = 'slug',
        read_only=True,
    )

    # price = serializers.IntegerField(validators=[ValidateQuantity])

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
        ]
      
        
