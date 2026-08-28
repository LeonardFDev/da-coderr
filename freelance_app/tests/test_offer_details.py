"""Tests for the offer details API."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from auth_app.models import Profile
from freelance_app.models import Offer, OfferDetail
from tests.helpers import status_code_with_message
from .datas import data_offer as OfferData

class OfferdetailsDetailGetTests(APITestCase):
    def setUp(self):
        self.user_business = User.objects.create_user(username="testuser_business", password="testpassword", email="testuser_business@test.de")
        self.profile_business = Profile.objects.create(user= self.user_business, username= self.user_business.username, email = self.user_business.email, type = "business", first_name= "Test", last_name="name")    

        self.token = Token.objects.create(user = self.user_business)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + self.token.key)

        OfferData.create_offer_objects(self.profile_business, Offer, OfferDetail, 3)
        
        self.offer = Offer.objects.all()[1]
        self.offer_detail_basic = OfferDetail.objects.all()[3]
        self.offer_detail_standard = OfferDetail.objects.all()[4]
        self.offer_detail_premium = OfferDetail.objects.all()[5]
        
    def test_offer_details_detail_get_401(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken")

        url = reverse("offerdetails-detail", kwargs={"id": self.offer_detail_basic.id}) 
        response = self.client.get(url)
                    
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offer_details_detail_get_404(self):
        url = reverse("offerdetails-detail", kwargs={"id": 999})
        response = self.client.get(url)
                        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_offer_details_detail_basic_get_200(self):
        url = reverse("offerdetails-detail", kwargs={"id": self.offer_detail_basic.id})
        response = self.client.get(url)
            
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_offer_details_detail_standard_get_200(self):
        url = reverse("offerdetails-detail", kwargs={"id": self.offer_detail_standard.id})
        response = self.client.get(url)
            
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_offer_details_detail_premium_get_200(self):
        url = reverse("offerdetails-detail", kwargs={"id": self.offer_detail_premium.id})
        response = self.client.get(url)
            
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)