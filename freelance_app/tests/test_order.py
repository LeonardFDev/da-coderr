from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from auth_app.models import Profile
from freelance_app.models import Offer, OfferDetail, Order
from tests.helpers import status_code_with_message
from .datas import data_offer as OfferData
from .datas import data_order as OrderData


class OrderListGetTests(APITestCase):
    def setUp(self):
        self.user_business = User.objects.create_user(username="testuser_business", password="testpassword", email="testuser_business@test.de")
        self.profile_business = Profile.objects.create(user= self.user_business, username= self.user_business.username, email = self.user_business.email, type = "business", first_name= "Test", last_name="name")

        self.user_customer = User.objects.create_user(username="testuser-customer", password="testpassword", email="testuser_customer@test.de")
        self.profile_customer = Profile.objects.create(user= self.user_customer, username= self.user_customer.username, email = self.user_customer.email, type = "customer", first_name= "Test", last_name="name")

        self.token = Token.objects.create(user = self.user_customer)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + self.token.key)

        OfferData.create_offer_objects(self.profile_business, Offer, OfferDetail, 4)
        OrderData.create_order_objects(self.profile_business, self.profile_customer, Offer, OfferDetail, Order, 4)

    def test_offer_list_get_401(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken")

        url = reverse("offer-list")
        response = self.client.get(url)
    
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_list_customer_get_200(self):
        url = reverse("order-list")
        response = self.client.get(url)
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_list_business_get_200(self):
        token = Token.objects.create(user = self.user_business)
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + token.key)

        url = reverse("order-list")
        response = self.client.get(url)
            
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_list_no_orders_get_200(self):
        user_no_orders = User.objects.create_user(username="testuser_no_orders", password="testpassword", email="testuser_no_orders@test.de")
        profile_no_orders = Profile.objects.create(user= user_no_orders, username= user_no_orders.username, email = user_no_orders.email, type = "business", first_name= "Test", last_name="name")
        
        token = Token.objects.create(user = user_no_orders)
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + token.key)
    
        url = reverse("order-list")
        response = self.client.get(url)
    
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OrderListPostTests(APITestCase):
    def setUp(self):
        self.user_business = User.objects.create_user(username="testuser_business", password="testpassword", email="testuser_business@test.de")
        self.profile_business = Profile.objects.create(user= self.user_business, username= self.user_business.username, email = self.user_business.email, type = "business", first_name= "Test", last_name="name")

        self.user_customer = User.objects.create_user(username="testuser-customer", password="testpassword", email="testuser_customer@test.de")
        self.profile_customer = Profile.objects.create(user= self.user_customer, username= self.user_customer.username, email = self.user_customer.email, type = "customer", first_name= "Test", last_name="name")

        self.token = Token.objects.create(user = self.user_customer)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + self.token.key)

        OfferData.create_offer_objects(self.profile_business, Offer, OfferDetail, 4)

    def test_order_list_incorrect_type_post_400(self):
        url = reverse("order-list")
        data = data = {"offer_detail_id": "abc"}
        response = self.client.post(url, data, format= "json")
                
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_list_required_post_400(self):
        url = reverse("order-list")
        data = data = {}
        response = self.client.post(url, data, format= "json")
                
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_offer_list_post_401(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken")
        
        url = reverse("order-list")
        data = {"offer_detail_id": 1}
        response = self.client.post(url, data, format= "json")
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offer_list_no_customer_post_403(self):
        user_business = User.objects.create_user(username="testuser2", password="testpassword", email="testuser2@test.de")
        profile_business = Profile.objects.create(user= user_business, username= user_business.username, email = user_business.email, type = "business")
                
        token = Token.objects.create(user = user_business)
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + token.key)
        
        url = reverse("order-list")
        data = {"offer_detail_id": 1}
        response = self.client.post(url, data, format= "json")
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offer_list_no_customer_post_404(self):
        url = reverse("order-list")
        data = {"offer_detail_id": 999}
        response = self.client.post(url, data, format= "json")
            
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_order_list_post_201(self):
        url = reverse("order-list")
        data = {"offer_detail_id": 1}
        response = self.client.post(url, data, format= "json")
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class OrderDetailPatchTests(APITestCase):
    def setUp(self):
        self.user_business = User.objects.create_user(username="testuser_business", password="testpassword", email="testuser_business@test.de")
        self.profile_business = Profile.objects.create(user= self.user_business, username= self.user_business.username, email = self.user_business.email, type = "business", first_name= "Test", last_name="name")

        self.user_customer = User.objects.create_user(username="testuser-customer", password="testpassword", email="testuser_customer@test.de")
        self.profile_customer = Profile.objects.create(user= self.user_customer, username= self.user_customer.username, email = self.user_customer.email, type = "customer", first_name= "Test", last_name="name")

        self.token = Token.objects.create(user = self.user_business)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + self.token.key)

        OfferData.create_offer_objects(self.profile_business, Offer, OfferDetail, 4)
        OrderData.create_order_objects(self.profile_business, self.profile_customer, Offer, OfferDetail, Order, 4)
        self.order = Order.objects.all()[2]

    def test_order_detail_incorrect_not_a_valid_choice_post_400(self):
        url = reverse("order-detail", kwargs={"id": self.order.id})
        data = {"status": "abc"}
        response = self.client.patch(url, data, format= "json")
                
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_detail_required_post_400(self):
        url = reverse("order-detail", kwargs={"id": self.order.id})
        data = data = {}
        response = self.client.patch(url, data, format= "json")
                
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_detail_post_401(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken")
        
        url = reverse("order-detail", kwargs={"id": self.order.id})
        data = {"status": "completed"}
        response = self.client.patch(url, data, format= "json")
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_detail_no_customer_post_403(self):
        user_business = User.objects.create_user(username="testuser2", password="testpassword", email="testuser2@test.de")
        profile_business = Profile.objects.create(user= user_business, username= user_business.username, email = user_business.email, type = "business")
                
        token = Token.objects.create(user = user_business)
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + token.key)
        
        url = reverse("order-detail", kwargs={"id": self.order.id})
        data = {"status": "completed"}
        response = self.client.patch(url, data, format= "json")
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_detail_post_404(self):
        url = reverse("order-detail", kwargs={"id": 999})
        data = {"status": "completed"}
        response = self.client.patch(url, data, format= "json")
            
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_order_detail_post_200(self):
        url = reverse("order-detail", kwargs={"id": self.order.id})
        data = {"status": "completed"}
        response = self.client.patch(url, data, format= "json")
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OrderDetailDeleteTests(APITestCase):
    def setUp(self):
        self.user_business = User.objects.create_user(username="testuser_business", password="testpassword", email="testuser_business@test.de")
        self.profile_business = Profile.objects.create(user= self.user_business, username= self.user_business.username, email = self.user_business.email, type = "business", first_name= "Test", last_name="name")

        self.user_customer = User.objects.create_user(username="testuser-customer", password="testpassword", email="testuser_customer@test.de")
        self.profile_customer = Profile.objects.create(user= self.user_customer, username= self.user_customer.username, email = self.user_customer.email, type = "customer", first_name= "Test", last_name="name")

        self.user_admin = User.objects.create_user(username="admin", password="password", email="admin@test.de", is_staff=True)
        self.token_admin = Token.objects.create(user = self.user_admin)
        
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + self.token_admin.key)

        OfferData.create_offer_objects(self.profile_business, Offer, OfferDetail, 4)
        OrderData.create_order_objects(self.profile_business, self.profile_customer, Offer, OfferDetail, Order, 4)
        self.order = Order.objects.all()[2]
        
    def test_offer_detail_delete_401(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken")

        url = reverse("order-detail", kwargs={"id": self.order.id})
        response = self.client.delete(url)
                    
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offer_detail_delete_403(self):
        user_no_admin = User.objects.create_user(username="testuser2", password="testpassword", email="testuser2@test.de")
        profile_no_admin = Profile.objects.create(user= user_no_admin, username= user_no_admin.username, email = user_no_admin.email, type = "business")

        token2 = Token.objects.create(user = user_no_admin)
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + token2.key)
            
        url = reverse("order-detail", kwargs={"id": self.order.id})
        response = self.client.delete(url)
                            
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offer_detail_delete_404(self):
        url = reverse("order-detail", kwargs={"id": 999})
        response = self.client.delete(url)
                        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_offer_detail_delete_204(self):
        url = reverse("order-detail", kwargs={"id": self.order.id})
        response = self.client.delete(url)
            
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class OrderCountDetailGetTests(APITestCase):
    def setUp(self):
        self.user_business = User.objects.create_user(username="testuser_business", password="testpassword", email="testuser_business@test.de")
        self.profile_business = Profile.objects.create(user= self.user_business, username= self.user_business.username, email = self.user_business.email, type = "business", first_name= "Test", last_name="name")

        self.user_customer = User.objects.create_user(username="testuser-customer", password="testpassword", email="testuser_customer@test.de")
        self.profile_customer = Profile.objects.create(user= self.user_customer, username= self.user_customer.username, email = self.user_customer.email, type = "customer", first_name= "Test", last_name="name")

        self.token = Token.objects.create(user = self.user_business)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + self.token.key)

        OfferData.create_offer_objects(self.profile_business, Offer, OfferDetail, 4)
        OrderData.create_order_selected_status_objects(self.profile_business, self.profile_customer, Offer, OfferDetail, Order, 4)

    def test_order_count_detail_get_401(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken")

        url = reverse("order-count-detail", kwargs={"business_user_id": self.profile_business.id}) 
        response = self.client.get(url)
                    
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_count_detail_get_404(self):
        url = reverse("order-count-detail", kwargs={"business_user_id": 999})
        response = self.client.get(url)
                        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_order_count_detail_get_200(self):
        url = reverse("order-count-detail", kwargs={"business_user_id": self.profile_business.id})
        response = self.client.get(url)
            
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CompletedOrderCountDetailGetTests(APITestCase):
    def setUp(self):
        self.user_business = User.objects.create_user(username="testuser_business", password="testpassword", email="testuser_business@test.de")
        self.profile_business = Profile.objects.create(user= self.user_business, username= self.user_business.username, email = self.user_business.email, type = "business", first_name= "Test", last_name="name")

        self.user_customer = User.objects.create_user(username="testuser-customer", password="testpassword", email="testuser_customer@test.de")
        self.profile_customer = Profile.objects.create(user= self.user_customer, username= self.user_customer.username, email = self.user_customer.email, type = "customer", first_name= "Test", last_name="name")

        self.token = Token.objects.create(user = self.user_business)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION= "Token " + self.token.key)

        OfferData.create_offer_objects(self.profile_business, Offer, OfferDetail, 4)
        OrderData.create_order_selected_status_objects(self.profile_business, self.profile_customer, Offer, OfferDetail, Order, 4)

    def test_completed_order_count_detail_get_401(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken")

        url = reverse("completed-order-count-detail", kwargs={"business_user_id": self.profile_business.id}) 
        response = self.client.get(url)
                    
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_completed_order_count_detail_get_404(self):
        url = reverse("completed-order-count-detail", kwargs={"business_user_id": 999})
        response = self.client.get(url)
                        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_completed_order_count_detail_get_200(self):
        url = reverse("completed-order-count-detail", kwargs={"business_user_id": self.profile_business.id})
        response = self.client.get(url)
            
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)