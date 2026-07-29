from django.db import models

from auth_app.models import Profile

class OfferDetail(models.Model):
    class OfferType(models.TextChoices):
        BASIC = "basic" ,"Basic"
        STANDARD = "standard", "Standard"
        PREMIUM = "premium", "Premium"

    title = models.CharField(max_length=100)
    revisions = models.IntegerField(blank=True, default=0)
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=20, choices=OfferType.choices, unique=True)

class Offer(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    detail = models.ForeignKey(OfferDetail, on_delete=models.CASCADE, related_name="offers")