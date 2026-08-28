"""Factories for creating sample data."""

import factory
import random
from itertools import product
from django.core.management import call_command
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from freelance_app.models import Offer, OfferDetail, Order, Review
from auth_app.models import Profile


def generate_working_hours():
    """returns random working days with primeval times"""
    working_days = [
        "Mo-Fr",
        "Mo-Sa",
        "Mo-So",
        "Di-Sa",
        "Di-So",
        "Mi-So",
        "Mo-Do",
        "Mo-Fr",
        "Mo, Mi, Fr",
        "Mo, Di, Do, Fr",
        "Mo, Di, Mi, Do, Fr",
        "Mo, Mi, Do, Sa",
        "Sa-So",
        "Fr-So",
    ]

    days = random.choice(working_days)

    start_hour = random.randint(7, 10)
    end_hour = random.randint(17, 21)

    return f"{days} {start_hour:02d}:00-{end_hour:02d}:00"

def generate_features():
    """Returns 2 to 5 random values from the features_values list"""
    features_values = [
        "Online-Buchung",
        "Terminverwaltung",
        "Online-Zahlung",
        "Kundenverwaltung",
        "Rechnungsstellung",
        "Benachrichtigungen",
        "E-Mail-Versand",
        "SMS-Benachrichtigungen",
        "Kalenderintegration",
        "Berichte",
        "Statistiken",
        "Datei-Upload",
        "Benutzerverwaltung",
        "Rollenverwaltung",
        "Mehrsprachigkeit",
        "Suchfunktion",
        "Favoriten",
        "Bewertungen",
        "Rabattcodes",
        "Gutscheine",
        "Live-Chat",
        "Kontaktformular",
        "API-Zugriff",
        "Export",
        "Import",
    ]

    return random.sample(
        features_values,
        k=random.randint(2, 5),
    )


class TokenFactory(factory.django.DjangoModelFactory):
    """Factory for creating Token model instances."""

    class Meta:
        model = Token


class ProfileFactory(factory.django.DjangoModelFactory):
    """Factory for creating Profile model instances."""

    username = factory.LazyAttribute(lambda obj: obj.user.username)
    email = factory.Faker("email")
    type = factory.Iterator(["customer","business"])
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    location = factory.Faker("city")
    tel = factory.Faker("numerify", text="015########")
    description = factory.Faker("paragraph", nb_sentences=3)
    working_hours = factory.LazyFunction(generate_working_hours)
    
    class Meta:
        model = Profile


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating User model instances."""

    @staticmethod
    def fixed_or_random_password(password = None):
        """returns the passing password or a random password"""
        if password is None:
            return factory.Faker("password")
        return password

    username = factory.Faker("user_name")
    password = factory.PostGenerationMethodCall("set_password", fixed_or_random_password("asdasd"))

    _token = factory.RelatedFactory(TokenFactory, "user")
    _profile = factory.RelatedFactory(ProfileFactory,"user")


    class Meta:
        model = User


class OfferDetailFactory(factory.django.DjangoModelFactory):
    """Factory for creating Offer detail model instances."""

    title = factory.Faker("sentence", nb_words=4)
    revisions = factory.Faker("random_int", min=-1, max=100)
    delivery_time_in_days = factory.Faker("random_int", min=3, max=17)
    price = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    features = factory.LazyFunction(generate_features)
    offer_type = factory.Iterator(["basic", "standard", "premium"])

    class Meta:
        model = OfferDetail


class OfferFactory(factory.django.DjangoModelFactory):
    """Factory for creating Offer model instances."""

    user = factory.Iterator(Profile.objects.filter(type = "business"))
    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph", nb_sentences=3)

    _offer_detail = factory.RelatedFactoryList(OfferDetailFactory,"offer",size=3)

    class Meta:
        model = Offer


class OrderFactory(factory.django.DjangoModelFactory):
    """Factory for creating Order model instances."""

    customer_user = factory.Iterator(Profile.objects.filter(type = "customer"))
    business_user = factory.Iterator(Profile.objects.filter(type = "business"))
    offer = factory.Iterator(Offer.objects.all())
    offer_detail = factory.LazyAttribute(lambda obj: OfferDetail.objects.filter(offer=obj.offer).order_by("?").first())
    status = factory.Iterator(["cancelled", "in_progress", "completed"])

    class Meta:
        model = Order


class ReviewFactory(factory.django.DjangoModelFactory):
    """Factory for creating Review model instances."""

    rating = factory.Faker("random_int", min=1, max=5)
    description = factory.Faker("paragraph", nb_sentences=3)

    class Meta:
        model = Review


def create_reviews():
    """Pass customer and business users to ReviewFactory and create instances of the review model"""
    customer_user = Profile.objects.filter(type = "customer")
    business_user = Profile.objects.filter(type = "business")

    for customer_user, business_user in product(customer_user, business_user):
        ReviewFactory(reviewer=customer_user, business_user=business_user)


def create_all():
    """empties the database first and creates new instances for all models"""
    call_command("flush", interactive=False)
    UserFactory.create_batch(10)
    OfferFactory.create_batch(15)
    OrderFactory.create_batch(30)
    create_reviews()