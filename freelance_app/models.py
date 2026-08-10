from django.db import models

from auth_app.models import Profile

class Offer(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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
    offer_type = models.CharField(max_length=20, choices=OfferType.choices)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="offer_details")


class Order(models.Model):
   class Status(models.TextChoices):
        OPEN = "open", "Open"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"
        REJECTED = "rejected", "Rejected"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed" ,"Completed"

   customer_user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="customer_user_orders")
   business_user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="business_user_orders")
   offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, related_name="offer_orders")
   offer_detail = models.ForeignKey(OfferDetail, on_delete=models.SET_NULL, null=True, related_name="offer_detail_orders")
   status = models.CharField(max_length=20, choices=Status.choices, default="in_progress")
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)