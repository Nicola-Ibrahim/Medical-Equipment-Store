from django.db.models import Sum

from core.apps.accounts.models import User
from core.apps.order.models import Order

from .models import Product


class ProductQuerySetMixin:

    def get_queryset(self, *args, **kwargs):
        """
        Display only related products to warehouse
        Display all products if the user is admin
        """

        qs = super().get_queryset(*args, **kwargs)

        if self.request.user.type not in [
            User.Type.ADMIN,
            User.Type.WAREHOUSE,
        ]:
            lookup_filter = dict()
            lookup_filter["visible"] = True
            qs = qs.filter(**lookup_filter)

        if self.request.user.type == User.Type.WAREHOUSE:
            lookup_filter = dict()
            lookup_filter["warehouse"] = self.request.user
            qs = qs.filter(**lookup_filter)

        return qs


class ProductsSoldQuerySetMixin:

    def get_queryset(self, *args, **kwargs):
        """
        This QuerySet display the number of products sold
        """
        qs = Product.objects.none()

        if self.request.user.type == User.Type.ADMIN:
            lookup_values = ["name", "warehouse"]
            qs = (Product.objects.values(*lookup_values).annotate(sold_count=Sum("product_set__quantity")).order_by())

        if self.request.user.type == User.Type.WAREHOUSE:
            lookup_filter = dict()
            lookup_filter["warehouse"] = self.request.user
            lookup_filter["product_set__isnull"] = False

            lookup_values = ["name", "warehouse"]

            # Create INNER JOIN between Product model and OrderProduct
            # model and aggregate with Sum()
            qs = (
                Product.objects.filter(**lookup_filter).values(*lookup_values
                                                               ).annotate(sold_count=Sum("product_set__quantity")
                                                                          ).order_by()
            )

        return qs
