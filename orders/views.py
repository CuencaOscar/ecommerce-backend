from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from products.models import Product

from .models import CartItem, Order, OrderItem
from .serializers import CartItemSerializer, OrderSerializer


def _cart_payload(user):
    items = CartItem.objects.filter(user=user).select_related("product")
    total = sum((item.subtotal for item in items), Decimal("0"))
    return {"items": CartItemSerializer(items, many=True).data, "total": f"{total:.2f}"}


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def cart(request):
    """The signed-in user's cart with its total."""
    return Response(_cart_payload(request.user))


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def add_to_cart(request):
    """Add a product, or increase its quantity if it is already in the cart."""
    product = get_object_or_404(Product, pk=request.data.get("product_id"))
    item = CartItem.objects.filter(user=request.user, product=product).first()
    quantity = int(request.data.get("quantity", 1)) + (item.quantity if item else 0)
    serializer = CartItemSerializer(item, data={"product_id": product.pk, "quantity": quantity})
    serializer.is_valid(raise_exception=True)
    serializer.save(user=request.user)
    return Response(_cart_payload(request.user), status=status.HTTP_201_CREATED)


@api_view(["PATCH", "DELETE"])
@permission_classes([permissions.IsAuthenticated])
def cart_item(request, pk):
    """Change the quantity of a cart item, or remove it."""
    item = get_object_or_404(CartItem, pk=pk, user=request.user)
    if request.method == "DELETE":
        item.delete()
    else:
        serializer = CartItemSerializer(item, data={"quantity": request.data.get("quantity")}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    return Response(_cart_payload(request.user))


@api_view(["GET", "POST"])
@permission_classes([permissions.IsAuthenticated])
def orders(request):
    """GET: the user's orders, newest first. POST: check out the current cart."""
    if request.method == "GET":
        return Response(OrderSerializer(Order.objects.filter(user=request.user).prefetch_related("items"), many=True).data)

    with transaction.atomic():
        items = list(CartItem.objects.filter(user=request.user).select_related("product").select_for_update())
        if not items:
            return Response({"detail": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)
        products = {p.pk: p for p in Product.objects.select_for_update().filter(pk__in=[i.product_id for i in items])}
        missing = [i.product.name for i in items if products[i.product_id].stock < i.quantity]
        if missing:
            return Response(
                {"detail": f"Not enough stock for: {', '.join(missing)}."}, status=status.HTTP_409_CONFLICT
            )
        order = Order.objects.create(user=request.user, total=sum((i.subtotal for i in items), Decimal("0")))
        for item in items:
            product = products[item.product_id]
            OrderItem.objects.create(
                order=order, product=product, name=product.name, unit_price=product.price, quantity=item.quantity
            )
            product.stock -= item.quantity
            product.save(update_fields=["stock"])
        CartItem.objects.filter(user=request.user).delete()
    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
