import random
from django.contrib.auth.models import User

from auth_app.models import Profile
from freelance_app.models import Review


test_review_data = {
    "business_user": 2,
    "rating": 4,
    "description": "Alles war toll!"
}

def create_review_customer_objects(reviewer, range_stop = 12):
    for review_number in range(1, range_stop):
        random_rating = random.choice([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
        user_business = User.objects.create_user(username=f"testuser_business(r{review_number})", password="testpassword", email=f"testuser_business(r{review_number})@test.de")
        profile_business = Profile.objects.create(user= user_business, username= user_business.username, email = user_business.email, type = "business", first_name= "Test", last_name="name")
        
        review = Review.objects.create(business_user = profile_business, reviewer = reviewer, rating = random_rating, description = f"Alles war toll({review_number})!")
    create_review_business_objects(range_stop)


def create_review_business_objects(range_stop):
    user_business = User.objects.create_user(username=f"rtestuser_business", password="testpassword", email=f"rtestuser_business@test.de")
    profile_business = Profile.objects.create(user= user_business, username= user_business.username, email = user_business.email, type = "business", first_name= "Test", last_name="name")

    for review_number in range(range_stop, range_stop * 2 - 1):
        random_rating = random.choice([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
        user_customer = User.objects.create_user(username=f"testuser_customer(r{review_number})", password="testpassword", email=f"testuser_customer(r{review_number})@test.de")
        profile_customer = Profile.objects.create(user= user_customer, username= user_customer.username, email = user_customer.email, type = "customer", first_name= "Test", last_name="name")
        review = Review.objects.create(business_user = profile_business, reviewer = profile_customer, rating = random_rating, description = f"Alles war toll({review_number})!")

def create_double_review_objects():
    profile_business = Profile.objects.get(id = 2)
    profile_reviewer = Profile.objects.get(id = 1)
    double_review = Review.objects.create(business_user = profile_business, reviewer = profile_reviewer, rating = 4, description = f"Alles war toll(1)!")