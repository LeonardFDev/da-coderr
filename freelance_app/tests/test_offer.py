from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from auth_app.models import Profile
from freelance_app.models import Offer, OfferDetail
from tests.helpers import status_code_with_message
from .datas import data_offer as OfferData


class OfferListGetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword", email="testuser@test.de")
        self.profile = Profile.objects.create(user= self.user, username= self.user.username, email = self.user.email, type = "customer", first_name= "Test", last_name="name")

        OfferData.create_offer_objects(self, Offer, OfferDetail, 12)
        
    def test_offer_list_get_400(self):
        url = reverse("offer-list")
        filter_search_ordering = {"creator_id": "a", "min_price": "c", "max_delivery_time": "abc", "page_size": "abc", "search": "django", "ordering": "created_at",}
        response = self.client.get(url, filter_search_ordering)
    
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_offer_list_get_200(self):
        url = reverse("offer-list")
        response = self.client.get(url)
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OfferListPostTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword", email="testuser@test.de")
        self.profile = Profile.objects.create(user= self.user, username= self.user.username, email = self.user.email, type = "business", first_name= "Test", last_name="name")

        self.token = Token.objects.create(user = self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + self.token.key)

    def test_offer_list_offer_type_double_value_post_400(self):
        url = reverse("offer-list")
        data = OfferData.test_offer_list_offer_type_double_value_post_400_data
        response = self.client.post(url, data, format= "json")
                
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_offer_list_no_three_details_objects_post_400(self):
        url = reverse("offer-list")
        data = OfferData.test_offer_list_no_three_details_objects_post_400_data
        response = self.client.post(url, data, format= "json")
                
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_offer_list_not_a_valid_choice_post_400(self):
        url = reverse("offer-list")
        data = OfferData.test_offer_list_not_a_valid_choice_post_400_data
        response = self.client.post(url, data, format= "json")

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_offer_list_no_values_post_400(self):
        url = reverse("offer-list")
        data = {}
        response = self.client.post(url, data, format= "json")
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_offer_list_post_401(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken")
        
        url = reverse("offer-list")
        data = OfferData.test_offer_list_post_401_data
        response = self.client.post(url, data, format= "json")
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offer_list_post_403(self):
        user2 = User.objects.create_user(username="testuser2", password="testpassword", email="testuser2@test.de")
        profile2 = Profile.objects.create(user= user2, username= user2.username, email = user2.email, type = "customer")
                
        token2 = Token.objects.create(user = user2)
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + token2.key)
        
        url = reverse("offer-list")
        data = OfferData.test_offer_list_post_403_data
        response = self.client.post(url, data, format= "json")
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_detail_post_201(self):
        url = reverse("offer-list")
        data = OfferData.test_profile_detail_post_201_data
        response = self.client.post(url, data, format= "json")
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class OfferDetailGetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword", email="testuser@test.de")
        self.profile = Profile.objects.create(user= self.user, username= self.user.username, email = self.user.email, type = "business", first_name= "Test", last_name="name")
    
        self.token = Token.objects.create(user = self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + self.token.key)

        OfferData.create_offer_objects(self, Offer, OfferDetail, 3)
        
        self.offer = Offer.objects.all()[1]
        
    def test_offer_detail_get_401(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken")

        url = reverse("offer-detail", kwargs={"id": self.offer.id}) 
        response = self.client.get(url)
                    
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offer_detail_get_404(self):
        url = reverse("offer-detail", kwargs={"id": 999})
        response = self.client.get(url)
                        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_offer_detail_get_200(self):
        url = reverse("offer-detail", kwargs={"id": self.offer.id})
        response = self.client.get(url)
            
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OfferDetailPatchTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword", email="testuser@test.de")
        self.profile = Profile.objects.create(user= self.user, username= self.user.username, email = self.user.email, type = "business", first_name= "Test", last_name="name")
    
        self.token = Token.objects.create(user = self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + self.token.key)

        OfferData.create_offer_objects(self, Offer, OfferDetail, 4)
        
        self.offer = Offer.objects.all()[2]

    def test_offer_detail_without_offer_type_patch_400(self):
        url = reverse("offer-detail", kwargs={"id": self.offer.id}) 
        data = OfferData.test_offer_detail_without_offer_type_patch_400_data
        response = self.client.patch(url, data, format= "json")
                    
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_offer_detail_with_wrong_value_patch_400(self):
        url = reverse("offer-detail", kwargs={"id": self.offer.id}) 
        data = OfferData.test_offer_detail_with_wrong_value_patch_400_data
        response = self.client.patch(url, data, format= "json")
                        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_offer_detail_multiple_offer_type_value_patch_400(self):
        url = reverse("offer-detail", kwargs={"id": self.offer.id}) 
        data = OfferData.test_offer_detail_multiple_offer_type_value_patch_400_data
        response = self.client.patch(url, data, format= "json")
                        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_offer_detail_patch_401(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken")

        url = reverse("offer-detail", kwargs={"id": self.offer.id}) 
        data = OfferData.test_offer_detail_patch_401_data
        response = self.client.patch(url, data, format= "json")
                    
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offer_detail_patch_403(self):
        user2 = User.objects.create_user(username="testuser2", password="testpassword", email="testuser2@test.de")
        profile2 = Profile.objects.create(user= user2, username= user2.username, email = user2.email, type = "customer")
                        
        token2 = Token.objects.create(user = user2)
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + token2.key)
        
        url = reverse("offer-detail", kwargs={"id": self.offer.id})
        data = OfferData.test_offer_detail_patch_403_data
        response = self.client.patch(url, data, format= "json")
                        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offer_detail_patch_404(self):
        url = reverse("offer-detail", kwargs={"id": 999})
        data = OfferData.test_offer_detail_patch_404_data
        response = self.client.patch(url, data, format= "json")
                        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_offer_detail_with_details_patch_200(self):
        url = reverse("offer-detail", kwargs={"id": self.offer.id})
        data = OfferData.test_offer_detail_with_details_patch_200_data
        response = self.client.patch(url, data, format= "json")
            
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_offer_detail_without_details_patch_200(self):
        url = reverse("offer-detail", kwargs={"id": self.offer.id})
        data = OfferData.test_offer_detail_without_details_patch_200_data
        response = self.client.patch(url, data, format= "json")
            
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OfferDetailDeleteTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword", email="testuser@test.de")
        self.profile = Profile.objects.create(user= self.user, username= self.user.username, email = self.user.email, type = "business", first_name= "Test", last_name="name")
    
        self.token = Token.objects.create(user = self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + self.token.key)

        OfferData.create_offer_objects(self, Offer, OfferDetail, 3)
        
        self.offer = Offer.objects.all()[1]
        
    def test_offer_detail_delete_401(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken")

        url = reverse("offer-detail", kwargs={"id": self.offer.id}) 
        response = self.client.delete(url)
                    
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offer_detail_delete_403(self):
            user2 = User.objects.create_user(username="testuser2", password="testpassword", email="testuser2@test.de")
            profile2 = Profile.objects.create(user= user2, username= user2.username, email = user2.email, type = "business")
                    
            token2 = Token.objects.create(user = user2)
            self.client.credentials(HTTP_AUTHORIZATION= "Token " + token2.key)
            
            url = reverse("offer-detail", kwargs={"id": self.offer.id})
            response = self.client.delete(url)
                            
            status_code_with_message(self, response)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offer_detail_delete_404(self):
        url = reverse("offer-detail", kwargs={"id": 999})
        response = self.client.delete(url)
                        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_offer_detail_delete_204(self):
        url = reverse("offer-detail", kwargs={"id": self.offer.id})
        response = self.client.delete(url)
            
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class offerdetailsDetailGetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword", email="testuser@test.de")
        self.profile = Profile.objects.create(user= self.user, username= self.user.username, email = self.user.email, type = "business", first_name= "Test", last_name="name")
    
        self.token = Token.objects.create(user = self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + self.token.key)

        OfferData.create_offer_objects(self, Offer, OfferDetail, 3)
        
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