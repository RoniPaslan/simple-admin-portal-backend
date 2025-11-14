from django.db import models
from django.conf import settings
from products.models import Product

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField()
    customer_name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50,
        choices=(("pending","Pending"),("completed","Completed"),("cancelled","Cancelled"))
    )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
