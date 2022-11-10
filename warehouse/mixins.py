from accounts.models import User
from .models import Product
from doctor.models import Order, OrderProduct


class ProductQuerySetMixin:
    def get_queryset(self, *args, **kwargs):
        """
        Display only related products to warehouse
        Display all products if the user is admin
        """
        
        qs = super().get_queryset(*args, **kwargs)

        if(self.request.user.type != User.Type.ADMIN):
            lookup_data = dict()
            lookup_data['warehouse'] = self.request.user
            qs = qs.filter(**lookup_data)
            
        return qs
    

class WarehouseOrdersQuerySetMixin:
    def get_queryset(self, *args, **kwargs):
        """
        Display only related orders to warehouse
        Display all products if the user is admin
        """
        
        qs = OrderProduct.objects.all()
        
        warehouse_products_qs = Product.objects.filter(warehouse=self.request.user)
        qs = qs.filter(product__in=warehouse_products_qs).select_related('order')
        order_ids = [item['order'] for item in qs.values('order')]
        qs = Order.objects.filter(id__in=order_ids)
        return qs