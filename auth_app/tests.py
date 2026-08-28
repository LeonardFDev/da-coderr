"""Tests for the authentication and registration API."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from auth_app.models import Profile
from tests.helpers import status_code_with_message

class RegistrationTests(APITestCase):
    def test_registration_get_405(self):
        url = reverse("registration")
        response = self.client.get(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_registration_patch_405(self):
        url = reverse("registration")
        response = self.client.patch(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_registration_put_405(self):
        url = reverse("registration")
        response = self.client.put(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
            
    def test_registration_delete_405(self):
        url = reverse("registration")
        response = self.client.delete(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_registration_post_201(self):
        url = reverse("registration")
        data = {"username": "testuser", "email": "testuser@test.de", "password": "testpassword", "repeated_password": "testpassword", "type": "customer"}
        response = self.client.post(url, data, format= "json")

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_passwords_not_match_post_400(self):
        url = reverse("registration")
        data = {"username": "testuser", "email": "testuser@test.de", "password": "123456", "repeated_password": "testpassword", "type": "customer"}
        response = self.client.post(url, data, format= "json")

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_valid_email_post_400(self):
        url = reverse("registration")
        data = {"username": "testuser", "email": "testuser.test.de", "password": "testpassword", "repeated_password": "testpassword", "type": "customer"}
        response = self.client.post(url, data, format= "json")

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_double_profile_post_400(self):
        user = User.objects.create_user(username="testuser", password="testpassword", email="testuser@test.de")
        Token.objects.create(user = user)
        Profile.objects.create(user = user, username=user.username, email = user.email, type = "customer")

        url = reverse("registration")
        data = {"username": "testuser", "email": "testuser@test.de", "password": "testpassword", "repeated_password": "testpassword", "type": "customer"}
        response = self.client.post(url, data, format= "json")
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(APITestCase):
    def test_login_get_405(self):
        url = reverse("login")
        response = self.client.get(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_login_patch_405(self):
        url = reverse("login")
        response = self.client.patch(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_login_put_405(self):
        url = reverse("login")
        response = self.client.put(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
                    
    def test_login_delete_405(self):
        url = reverse("login")
        response = self.client.delete(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_login_post_200(self):
        user = User.objects.create_user(username="testuser", password="testpassword", email="testuser@test.de")
        Token.objects.create(user = user)
        Profile.objects.create(user = user, username=user.username, email = user.email, type = "customer")
    
        url = reverse("login")
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(url, data, format= "json")

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)