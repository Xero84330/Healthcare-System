from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()


class AuthTests(APITestCase):

    def test_register_then_login_returns_tokens(self):
        register_res = self.client.post("/api/auth/register/", {
            "name": "Alice",
            "email": "alice@example.com",
            "password": "StrongPass123!",
        })
        self.assertEqual(register_res.status_code, status.HTTP_201_CREATED)

        login_res = self.client.post("/api/auth/login/", {
            "email": "alice@example.com",
            "password": "StrongPass123!",
        })
        self.assertEqual(login_res.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", login_res.data)
        self.assertIn("refresh_token", login_res.data)

    def test_login_with_wrong_password_fails(self):
        User.objects.create_user(email="bob@example.com", name="Bob", password="StrongPass123!")

        login_res = self.client.post("/api/auth/login/", {
            "email": "bob@example.com",
            "password": "WrongPassword!",
        })
        self.assertEqual(login_res.status_code, status.HTTP_400_BAD_REQUEST)
