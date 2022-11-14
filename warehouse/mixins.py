from accounts.models import User
from .models import Product
from doctor.models import Order


class ProductQuerySetMixin:
    def get_queryset(self, *args, **kwargs):
        """
        Display only related products to warehouse
        Display all products if the user is admin
        """

        qs = Product.objects.none()

        if(self.request.user.type == User.Type.ADMIN):
            qs = super().get_queryset(*args, **kwargs)

        if(self.request.user.type == User.Type.WAREHOUSE):
            lookup_filter = dict()
            lookup_filter['warehouse'] = self.request.user
            qs = qs.filter(**lookup_filter)
            
        return qs
    

class WarehouseOrdersQuerySetMixin:
    def get_queryset(self, *args, **kwargs):
        """
        Display only related orders to warehouse
        Display all products if the user is admin
        """
        qs = Order.objects.none()

        # If the user is admin
        # Display all orders related to warehouses
        if(self.request.user.type == User.Type.ADMIN):
            qs = Order.objects.all()

        # If the use is warehouse
        # Display ONLY related orders
        if(self.request.user.type == User.Type.WAREHOUSE):
            lookup_filter = dict()
            lookup_filter['warehouse'] = self.request.user
            lookup_filter['product_set__isnull'] = False

            lookup_values = ['name', 'product_set__order', 'product_set__order__price']


            # Create INNER JOIN between Product model and OrderProduct model
            products_qs = Product.objects.filter(**lookup_filter).values_list(*lookup_values)

            # TODO: Customize the way of displaying the order 
            # TODO: <QuerySet [('Tea1', 71, 4600.0), ('Coffee1', 71, 4600.0), ('Coffee1', 73, 1650.0)]>

            order_ids = [item[1] for item in products_qs]
            qs = Order.objects.filter(id__in=order_ids)
            print(qs)
        
        return qs