from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from .models import Product


class ProductApiTests(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Keyboard", description="Mechanical", price="89.50", stock=4)
        self.payload = {"name": "Mouse", "description": "Wireless", "price": "25.00", "stock": 10}

    def test_anyone_can_browse_the_catalog(self):
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["name"], "Keyboard")

    def test_product_detail_and_not_found(self):
        self.assertEqual(self.client.get(f"/api/products/{self.product.pk}/").status_code, 200)
        self.assertEqual(self.client.get("/api/products/9999/").status_code, 404)

    def test_customers_cannot_modify_the_catalog(self):
        self.assertEqual(self.client.post("/api/products/", self.payload).status_code, 401)
        customer = get_user_model().objects.create_user("ana@example.com", password="s3cure-pass!")
        self.client.force_authenticate(customer)
        self.assertEqual(self.client.post("/api/products/", self.payload).status_code, 403)
        self.assertEqual(self.client.delete(f"/api/products/{self.product.pk}/").status_code, 403)

    def test_staff_can_manage_products(self):
        staff = get_user_model().objects.create_user("admin@example.com", password="s3cure-pass!", is_staff=True)
        self.client.force_authenticate(staff)
        self.assertEqual(self.client.post("/api/products/", self.payload).status_code, 201)
        self.assertEqual(self.client.delete(f"/api/products/{self.product.pk}/").status_code, 204)


class ApiDocsTests(APITestCase):
    def test_openapi_schema_and_swagger_ui_are_served(self):
        schema = self.client.get("/api/schema/?format=json")
        self.assertEqual(schema.status_code, 200)
        paths = schema.json()["paths"]
        for path in ("/api/products/", "/api/auth/token/", "/api/cart/", "/api/orders/"):
            self.assertIn(path, paths)
        self.assertEqual(self.client.get("/api/docs/").status_code, 200)


class SeedProductsTests(APITestCase):
    def test_demo_catalog_has_photos_and_is_idempotent(self):
        from django.core.management import call_command

        call_command("seed_products", verbosity=0)
        call_command("seed_products", verbosity=0)
        products = self.client.get("/api/products/").json()
        self.assertEqual(len(products), 8)
        self.assertTrue(all(p["image_url"].startswith("https://images.unsplash.com/") for p in products))
