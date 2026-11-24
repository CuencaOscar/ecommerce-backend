from django.urls import path

from . import views

urlpatterns = [
    path("cart/", views.cart, name="cart"),
    path("cart/items/", views.add_to_cart, name="cart-add"),
    path("cart/items/<int:pk>/", views.cart_item, name="cart-item"),
    path("orders/", views.orders, name="orders"),
]
