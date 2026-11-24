from rest_framework import serializers

from products.models import Product
from products.serializers import ProductSerializer

from .models import CartItem, Order, OrderItem


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source="product", write_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_id", "quantity", "subtotal"]

    def validate(self, attrs):
        product = attrs.get("product") or self.instance.product
        quantity = attrs.get("quantity", getattr(self.instance, "quantity", 1))
        if quantity < 1:
            raise serializers.ValidationError({"quantity": "Quantity must be at least 1."})
        if quantity > product.stock:
            raise serializers.ValidationError({"quantity": f"Only {product.stock} units of {product.name} left."})
        return attrs


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "name", "unit_price", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "status", "total", "created_at", "items"]
