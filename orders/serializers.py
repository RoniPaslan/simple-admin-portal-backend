# orders/serializers.py
from rest_framework import serializers
from .models import Order
from products.serializers import ProductSerializer
from products.models import Product
from users.serializers import UserSerializer

class OrderSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "product",
            "quantity",
            "customer_name",
            "status",
            "created_by",
            "created_at",
        ]
        read_only_fields = ["id", "created_by", "created_at"]

    def to_representation(self, instance):
        """Override untuk nested product di output, sertakan context request"""
        rep = super().to_representation(instance)
        # sertakan context supaya get_image bisa build_absolute_uri
        rep['product'] = ProductSerializer(instance.product, context=self.context).data
        return rep
