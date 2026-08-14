test_profile_data = {
    "first_name": "Max",
    "last_name": "Mustermann",
    "location": "Berlin",
    "tel": "987654321",
    "description": "Updated business description",
    "working_hours": "10-18",
    "email": "new_email@business.de"
}


def create_profile_customer_objects(User, Profile, range_stop = 12):
    for profile_number in range(1, range_stop):
        user = User.objects.create_user(username=f"testuser_business({profile_number})", password="testpassword", email=f"testuser_business({profile_number})@test.de")
        Profile.objects.create(user= user, username= user.username, email = user.email, type = type_changer(profile_number), first_name= "Test", last_name="name")

def type_changer(profile_number):
    if profile_number % 2 == 0:
        return "business"
    else: 
        return "customer"