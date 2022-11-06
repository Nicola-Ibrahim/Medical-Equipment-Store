from accounts.models import User

class WarehouseQuerySetMixin:
    def get_queryset(self, *args, **kwargs):
        """
        Display only related products to warehouse
        Display all products if the user is admin
        """
        
        qs = super().get_queryset(*args, **kwargs)

        print(self.request.user)
        if(self.request.user.type != User.Type.ADMIN):
            lookup_data = dict()
            lookup_data['warehouse'] = self.request.user
            qs = qs.filter(**lookup_data)
            
        return qs