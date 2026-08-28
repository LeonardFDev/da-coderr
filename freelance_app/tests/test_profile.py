"""Tests for the Profile API."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from auth_app.models import Profile
from tests.helpers import status_code_with_message
from .datas import data_profile as ProfileData


class ProfileGetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword", email="testuser@test.de")
        self.profile = Profile.objects.create(user= self.user, username= self.user.username, email = self.user.email, type = "customer")

        self.token = Token.objects.create(user = self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + self.token.key)

    def test_profile_detail_get_401(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken")

        url = reverse("profile-detail", kwargs={"pk": self.profile.id})
        response = self.client.get(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_detail_get_404(self):
        url = reverse("profile-detail", kwargs={"pk": 999})
        response = self.client.get(url)
    
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_profile_detail_get_200(self):
        url = reverse("profile-detail", kwargs={"pk": self.profile.id})
        response = self.client.get(url)
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfilePatchTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword", email="testuser@test.de")
        self.profile = Profile.objects.create(user= self.user, username= self.user.username, email = self.user.email, type = "customer")

        self.token = Token.objects.create(user = self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + self.token.key)

    def test_profile_detail_patch_401(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken")

        url = reverse("profile-detail", kwargs={"pk": self.profile.id})
        data = ProfileData.test_profile_data
        response = self.client.patch(url, data, format= "json")

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_detail_patch_403(self):
        user2 = User.objects.create_user(username="testuser2", password="testpassword", email="testuser2@test.de")
        profile2 = Profile.objects.create(user= user2, username= user2.username, email = user2.email, type = "customer")
        
        token2 = Token.objects.create(user = user2)
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + token2.key)
        
        url = reverse("profile-detail", kwargs={"pk": self.profile.id})
        data = ProfileData.test_profile_data
        response = self.client.patch(url, data, format= "json")
    
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_detail_patch_404(self):
        url = reverse("profile-detail", kwargs={"pk": 999})
        data = ProfileData.test_profile_data
        response = self.client.patch(url, data, format= "json")
    
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_profile_detail_patch_200(self):
        url = reverse("profile-detail", kwargs={"pk": self.profile.id})
        data = ProfileData.test_profile_data
        response = self.client.patch(url, data, format= "json")
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfilesBusinessTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword", email="testuser@test.de")
        self.profile = Profile.objects.create(user= self.user, username= self.user.username, email = self.user.email, type = "customer")

        self.token = Token.objects.create(user = self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + self.token.key)

        ProfileData.create_profile_objects(User, Profile, 9)

    def test_business_list_get_401(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken")

        url = reverse("profiles-business-list")
        response = self.client.get(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_business_list_get_200(self):
        url = reverse("profiles-business-list")
        response = self.client.get(url)
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_business_empty_list_get_200(self):
        Profile.objects.filter(type = "business").delete()
        url = reverse("profiles-business-list")
        response = self.client.get(url)
                
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfilesCustomerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword", email="testuser@test.de")
        self.profile = Profile.objects.create(user= self.user, username= self.user.username, email = self.user.email, type = "customer")

        self.token = Token.objects.create(user = self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + self.token.key)

        ProfileData.create_profile_objects(User, Profile, 9)

    def test_customer_list_get_401(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken")

        url = reverse("profiles-customer-list")
        response = self.client.get(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_customer_list_get_200(self):
        url = reverse("profiles-customer-list")
        response = self.client.get(url)
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_empty_list_get_200(self):
        Profile.objects.filter(type = "customer").delete()
        url = reverse("profiles-customer-list")
        response = self.client.get(url)
            
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)