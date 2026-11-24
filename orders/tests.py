from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from products.models import Product

from .models import Order


class CartAndCheckoutTests(APITestCase):
    def setUp(self):
        users = get_user_model().objects
        self.ana = users.create_user("ana@example.com", password="s3cure-pass!")
        self.bob = users.create_user("bob@example.com", password="s3cure-pass!")
        self.keyboard = Product.objects.create(name="Keyboard", description="", price="89.50", stock=3)
        self.hub = Product.objects.create(name="USB-C Hub", description="", price="45.00", stock=10)
        self.client.force_authenticate(self.ana)

    def add(self, product, quantity=1):
        return self.client.post("/api/cart/items/", {"product_id": product.pk, "quantity": quantity})

    def test_cart_requires_authentication(self):
        self.client.force_authenticate(None)
        self.assertEqual(self.client.get("/api/cart/").status_code, 401)

    def test_adding_the_same_product_increases_quantity_and_total(self):
        self.add(self.keyboard)
        response = self.add(self.keyboard)
        self.assertEqual(response.status_code, 201)
        cart = response.json()
        self.assertEqual(cart["items"][0]["quantity"], 2)
        self.assertEqual(cart["total"], "179.00")

    def test_cannot_add_more_than_the_stock(self):
        self.assertEqual(self.add(self.keyboard, 4).status_code, 400)

    def test_update_and_remove_items(self):
        item_id = self.add(self.hub).json()["items"][0]["id"]
        self.assertEqual(self.client.patch(f"/api/cart/items/{item_id}/", {"quantity": 5}).json()["total"], "225.00")
        self.assertEqual(self.client.delete(f"/api/cart/items/{item_id}/").json()["items"], [])

    def test_users_cannot_touch_other_carts(self):
        item_id = self.add(self.hub).json()["items"][0]["id"]
        self.client.force_authenticate(self.bob)
        self.assertEqual(self.client.delete(f"/api/cart/items/{item_id}/").status_code, 404)

    def test_checkout_creates_order_updates_stock_and_empties_cart(self):
        self.add(self.keyboard, 2)
        self.add(self.hub, 1)
        response = self.client.post("/api/orders/")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["total"], "224.00")
        self.keyboard.refresh_from_db()
        self.assertEqual(self.keyboard.stock, 1)
        self.assertEqual(self.client.get("/api/cart/").json()["items"], [])
        self.assertEqual(len(self.client.get("/api/orders/").json()), 1)

    def test_checkout_fails_without_items_or_stock(self):
        self.assertEqual(self.client.post("/api/orders/").status_code, 400)
        self.add(self.keyboard, 3)
        Product.objects.filter(pk=self.keyboard.pk).update(stock=1)
        self.assertEqual(self.client.post("/api/orders/").status_code, 409)
        self.assertEqual(Order.objects.count(), 0)

    def test_orders_are_private(self):
        self.add(self.hub)
        self.client.post("/api/orders/")
        self.client.force_authenticate(self.bob)
        self.assertEqual(self.client.get("/api/orders/").json(), [])
