
class WarehouseQuerySetMixin:
    def get_queryset(self, *args, **kwargs):
        lookup_data = dict()
        qs = super().get_queryset(*args, **kwargs)
        lookup_data['warehouse'] = self.request.user
        return qs.filter(**lookup_data)