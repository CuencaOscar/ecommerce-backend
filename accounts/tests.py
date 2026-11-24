from rest_framework.test import APITestCase


class AccountApiTests(APITestCase):
    def register(self, email="ana@example.com", password="s3cure-pass!"):
        return self.client.post("/api/auth/register/", {"name": "Ana", "email": email, "password": password})

    def test_register_returns_tokens_and_profile(self):
        response = self.register()
        self.assertEqual(response.status_code, 201)
        body = response.json()
        self.assertEqual(body["user"]["email"], "ana@example.com")
        self.assertIn("access", body)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {body['access']}")
        self.assertEqual(self.client.get("/api/auth/me/").json()["name"], "Ana")

    def test_duplicate_email_and_weak_password_are_rejected(self):
        self.register()
        self.assertEqual(self.register(email="ANA@example.com").status_code, 400)
        self.assertEqual(self.register(email="bob@example.com", password="12345678").status_code, 400)

    def test_login_with_email_and_password(self):
        self.register()
        response = self.client.post("/api/auth/token/", {"username": "ana@example.com", "password": "s3cure-pass!"})
        self.assertEqual(response.status_code, 200)
        bad = self.client.post("/api/auth/token/", {"username": "ana@example.com", "password": "wrong"})
        self.assertEqual(bad.status_code, 401)

    def test_profile_requires_authentication(self):
        self.assertEqual(self.client.get("/api/auth/me/").status_code, 401)
