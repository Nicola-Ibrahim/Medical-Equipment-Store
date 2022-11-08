from accounts.models import User
from .models import Product

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
        
        qs = super().get_queryset(*args, **kwargs)
        
        warehouse_products_qs = Product.objects.filter(warehouse=self.request.user)
        qs = qs.select_related('order').filter(product__in=warehouse_products_qs)

        return qs