from apps.accounts.models import User


class OrderQuerySetMixin:
    """
    This queryset mixin displays orders
    If the user is a admin then display all orders
    If the user is a doctor then only display its orders
    """

    def get_queryset(self, *args, **kwargs):
        # Order queryset
        qs = super().get_queryset(*args, **kwargs)

        match self.request.user.type:
            case User.Type.DOCTOR:  # display its orders
                lookup_data = dict()
                lookup_data["doctor"] = self.request.user
                qs = qs.filter(**lookup_data)

            case User.Type.WAREHOUSE:  # display ONLY related orders
                lookup_filter = dict()
                lookup_filter["product_set__isnull"] = False

                warehouse_user = self.request.user

                # Create INNER JOIN between Product model and OrderProduct model
                order_ids = warehouse_user.products.filter(**lookup_filter).values_list(
                    "product_set__order", flat=True
                )

                qs = qs.filter(id__in=set(order_ids))

        return qs
