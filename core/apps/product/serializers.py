from rest_framework import serializers

from core.apps.accounts.models import Warehouse

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="product:details",
        lookup_field="slug",
        read_only=True,
    )

    warehouse_name = serializers.ReadOnlyField(source="warehouse.warehouse_profile.name")

    class Meta:
        model = Product
        fields = [
            "id",
            "url",
            "name",
            "price",
            "image",
            "discount",
            "quantity",
            "visible",
            "slug",
            "created_at",
            "updated_at",
            "warehouse_name",
            "warehouse",
        ]
        read_only_fields = ["url", "slug", "created_at", "updated_at"]
        extra_kwargs = {
            "warehouse": {
                "write_only": True
            },
        }

    # def to_internal_value(self, data):
    #     """Change data attributes value"""

    #     # Assign warehouse field to current user
    #     data['warehouse'] = self.context['request'].user.id

    #     return super().to_internal_value(data)


class ProductsSoldSerializer(serializers.Serializer):
    """
    This serializer handles the display of products sold to the warehouse
    """

    name = serializers.CharField(read_only=True)
    sold_count = serializers.IntegerField(read_only=True)

    warehouse_name = serializers.SerializerMethodField()

    def get_warehouse_name(self, obj):
        qs = Warehouse.objects.get(id=obj["warehouse"])
        name = qs.warehouse_profile.name
        return name
