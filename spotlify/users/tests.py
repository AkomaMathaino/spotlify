from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
import json


# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        # Create data to be used in tests
        self.user_data = {
            "username": "testusername",
            "password": "testpassword",
            "email": "testemail@gmail.com",
        }

        self.new_info = {"username": "newusername", "email": "newemail@gmail.com"}

        self.verification_info = {"name": "John", "bio": "test bio"}

    def test_user(self):
        # Test registration
        response = self.client.post(
            reverse("register"),
            json.dumps(self.user_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertEqual(response.json()["username"], self.user_data["username"])

        # Test login
        self.user_data.pop("email")

        response = self.client.post(
            reverse("login"),
            json.dumps(self.user_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])

        # Test user info retrieval
        response = self.client.get(reverse("user_info", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], self.user_data["username"])

        # Test user info update
        response = self.client.put(
            reverse("update_info", args=[1]),
            json.dumps(self.new_info),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "User info updated successfully")

        # Test logout
        response = self.client.post(reverse("logout"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["logout"], "successful")

    def test_verification_request(self):
        # Test verification request
        User = get_user_model()
        user = User.objects.create(username="john", password="password")
        user.is_staff = True
        user.save()
        self.client.force_login(user)
        self.verification_info["user"] = user.id

        response = self.client.post(
            reverse("verification_request", args=[user.id]),
            json.dumps(self.verification_info),
            content_type="application/json",
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["message"], "verification request submitted successfully"
        )

        # Test verification request retrieval
        response = self.client.get(reverse("verification_requests"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["user"], user.username)

        # Test verification request approval
        response = self.client.patch(
            reverse("verification_request_approval", args=[user.id]),
            json.dumps({"approval_status": "approved"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["is verified"])
