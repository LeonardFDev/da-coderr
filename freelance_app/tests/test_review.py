"""Tests for the Review API."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from auth_app.models import Profile
from freelance_app.models import Review
from tests.helpers import status_code_with_message
from .datas import data_review as ReviewData


class ReviewListGetTests(APITestCase):
    def setUp(self):
        self.user_customer = User.objects.create_user(username="testuser-customer", password="testpassword", email="testuser_customer@test.de")
        self.profile_customer = Profile.objects.create(user= self.user_customer, username= self.user_customer.username, email = self.user_customer.email, type = "customer", first_name= "Test", last_name="name")

        self.token = Token.objects.create(user = self.user_customer)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + self.token.key)

        ReviewData.create_review_customer_objects(self.profile_customer, 4)

    def test_review_list_filters_a_string_get_400(self):
        url = reverse("review-list")
        filter_ordering = {"business_user_id": "a", "reviewer_id": "c", "ordering": "created_at"}
        response = self.client.get(url, filter_ordering)
    
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_list_get_401(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken")

        url = reverse("review-list")
        filter_ordering = {"business_user_id": "1", "reviewer_id": "2", "ordering": "updated_at"}
        response = self.client.get(url, filter_ordering)
    
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_list_empty_get_200(self):
        url = reverse("order-list")
        filter_ordering = {"business_user_id": "998", "reviewer_id": "999", "ordering": "updated_at"}
        response = self.client.get(url, filter_ordering)
    
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list_filter_ordering_both_filters_get_200(self):
        url = reverse("review-list")
        filter_ordering = {"business_user_id": "2", "reviewer_id": "1", "ordering": "rating"}
        response = self.client.get(url, filter_ordering)
            
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list_filter_ordering_business_filter_get_200(self):
        url = reverse("review-list")
        filter_ordering = {"business_user_id": 5, "ordering": "rating"}
        response = self.client.get(url, filter_ordering)
                
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list_filter_ordering_reviewer_filter_get_200(self):
        url = reverse("review-list")
        filter_ordering = {"reviewer_id": 1, "ordering": "updated_at"}
        response = self.client.get(url, filter_ordering)
                
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list_get_200(self):
        url = reverse("review-list")
        response = self.client.get(url)
                
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ReviewListPostTests(APITestCase):
    def setUp(self):
        self.user_customer = User.objects.create_user(username="testuser-customer", password="testpassword", email="testuser_customer@test.de")
        self.profile_customer = Profile.objects.create(user= self.user_customer, username= self.user_customer.username, email = self.user_customer.email, type = "customer", first_name= "Test", last_name="name")

        self.user_business = User.objects.create_user(username="testuser_business", password="testpassword", email="testuser_business@test.de")
        self.profile_business = Profile.objects.create(user= self.user_business, username= self.user_business.username, email = self.user_business.email, type = "business", first_name= "Test", last_name="name")

        self.token = Token.objects.create(user = self.user_customer)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + self.token.key)

    def test_review_list_post_400(self):
        Review.objects.create(business_user = self.profile_business, reviewer = self.profile_customer, rating = 4, description = f"Alles war toll!")

        url = reverse("review-list")
        data = ReviewData.test_review_data
        response = self.client.post(url, data, format= "json")
    
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)    

    def test_review_list_post_401(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken")

        url = reverse("review-list")
        data = ReviewData.test_review_data
        response = self.client.post(url, data, format= "json")
    
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_list_post_403(self):
        user_business = User.objects.create_user(username="testuser-business123", password="testpassword", email="testuser_business123@test.de")
        profile_business = Profile.objects.create(user= user_business, username= user_business.username, email = user_business.email, type = "business", first_name= "Test", last_name="name")
                    
        token_business = Token.objects.create(user = user_business)
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + token_business.key)
            
        url = reverse("review-list")
        data = ReviewData.test_review_data
        response = self.client.post(url, data, format= "json")
            
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_list_post_201(self):
        url = reverse("review-list")
        data = ReviewData.test_review_data
        response = self.client.post(url, data, format= "json")
                
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ReviewDetailPatchTests(APITestCase):
    def setUp(self):
        self.user_customer = User.objects.create_user(username="testuser-customer", password="testpassword", email="testuser_customer@test.de")
        self.profile_customer = Profile.objects.create(user= self.user_customer, username= self.user_customer.username, email = self.user_customer.email, type = "customer", first_name= "Test", last_name="name")
        
        self.token = Token.objects.create(user = self.user_customer)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + self.token.key)
        
        ReviewData.create_review_customer_objects(self.profile_customer, 4)
        self.review = Review.objects.all()[0]

    def test_review_detail_post_400(self):
        url = reverse("review-detail", kwargs={"pk": self.review.id})
        data = {"rating": "abc"}
        response = self.client.patch(url, data, format= "json")
                
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_detail_post_401(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken")
        
        url = reverse("review-detail", kwargs={"pk": self.review.id})
        data = {"rating": 1, "description": "Noch besser als erwartet!"}
        response = self.client.patch(url, data, format= "json")
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_detail_post_403(self):
        user_business = User.objects.create_user(username="testuser2", password="testpassword", email="testuser2@test.de")
        profile_business = Profile.objects.create(user= user_business, username= user_business.username, email = user_business.email, type = "business")
                
        token = Token.objects.create(user = user_business)
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + token.key)
        
        url = reverse("review-detail", kwargs={"pk": self.review.id})
        data = {"rating": 1, "description": "Noch besser als erwartet!"}
        response = self.client.patch(url, data, format= "json")
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_detail_post_404(self):
        url = reverse("review-detail", kwargs={"pk": 999})
        data = {"rating": 1, "description": "Noch besser als erwartet!"}
        response = self.client.patch(url, data, format= "json")
            
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_review_detail_post_200(self):
        url = reverse("review-detail", kwargs={"pk": self.review.id})
        data = {"rating": 1, "description": "Noch besser als erwartet!"}
        response = self.client.patch(url, data, format= "json")
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ReviewDetailDeleteTests(APITestCase):
    def setUp(self):
        self.user_customer = User.objects.create_user(username="testuser-customer", password="testpassword", email="testuser_customer@test.de")
        self.profile_customer = Profile.objects.create(user= self.user_customer, username= self.user_customer.username, email = self.user_customer.email, type = "customer", first_name= "Test", last_name="name")
            
        self.token = Token.objects.create(user = self.user_customer)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + self.token.key)
            
        ReviewData.create_review_customer_objects(self.profile_customer, 4)
        self.review = Review.objects.all()[0]
        
    def test_review_detail_delete_401(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken")

        url = reverse("review-detail", kwargs={"pk": self.review.id})
        response = self.client.delete(url)
                    
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_detail_delete_403(self):
        user_another_customer = User.objects.create_user(username="testuser2", password="testpassword", email="testuser2@test.de")
        profile_another_customer = Profile.objects.create(user= user_another_customer, username= user_another_customer.username, email = user_another_customer.email, type = "customer")

        token_another_customer = Token.objects.create(user = user_another_customer)
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + token_another_customer.key)
            
        url = reverse("review-detail", kwargs={"pk": self.review.id})
        response = self.client.delete(url)
                            
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_detail_delete_404(self):
        url = reverse("review-detail", kwargs={"pk": 999})
        response = self.client.delete(url)
                        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_review_detail_delete_204(self):
        url = reverse("review-detail", kwargs={"pk": self.review.id})
        response = self.client.delete(url)
            
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)