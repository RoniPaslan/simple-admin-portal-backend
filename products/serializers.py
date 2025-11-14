from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "stock", "created_by_username", "image", "image_url", "created_by", "created_at"]
        read_only_fields = ["id", "created_by", "created_at"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
