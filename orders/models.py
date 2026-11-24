from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from products.models import Product


class CartItem(models.Model):
    """A product in a customer's cart. One row per product and user."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "product"], name="unique_cart_product")]
        ordering = ["id"]

    @property
    def subtotal(self) -> Decimal:
        return self.product.price * self.quantity


class Order(models.Model):
    class Status(models.TextChoices):
        PLACED = "placed", "Placed"
        SHIPPED = "shipped", "Shipped"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLACED)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"Order #{self.pk} ({self.user})"


class OrderItem(models.Model):
    """Snapshot of a product at checkout time, so later price changes do not alter past orders."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
