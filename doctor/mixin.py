from accounts.models import User

class OrderQuerySetMixin:
    def get_queryset(self, *args, **kwargs):
        """
        Display only related products to warehouse
        Display all products if the user is admin
        """
        
        qs = super().get_queryset(*args, **kwargs)

        if(self.request.user.type != User.Type.ADMIN):
            lookup_data = dict()
            lookup_data['doctor'] = self.request.user
            qs = qs.filter(**lookup_data)
        
        return qs