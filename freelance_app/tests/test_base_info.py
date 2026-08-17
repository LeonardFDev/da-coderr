from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from auth_app.models import Profile
from tests.helpers import status_code_with_message
from freelance_app.models import Offer, OfferDetail
from .datas import data_review as ReviewData
from .datas import data_profile as ProfileData
from .datas import data_offer as OfferData


class BaseInfoListGetTests(APITestCase):
    def prepare_data(self):
        user_customer = User.objects.create_user(username="testuser-customer", password="testpassword", email="testuser_customer@test.de")
        profile_customer = Profile.objects.create(user= user_customer, username= user_customer.username, email = user_customer.email, type = "customer", first_name= "Test", last_name="name")
        
        user_business = User.objects.create_user(username="testuser_business", password="testpassword", email="testuser_business@test.de")
        profile_business = Profile.objects.create(user= user_business, username= user_business.username, email = user_business.email, type = "business", first_name= "Test", last_name="name")
        
        ReviewData.create_review_customer_objects(profile_customer, 4)
        ProfileData.create_profile_objects(User, Profile, 8)
        OfferData.create_offer_objects(profile_business, Offer, OfferDetail, 11)

    def test_base_info_list_get_200(self):
        self.prepare_data()
        url = reverse("base-info-list")
        response = self.client.get(url)
                
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_base_info_list_count_0_get_200(self):
        url = reverse("base-info-list")
        response = self.client.get(url)
                
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)