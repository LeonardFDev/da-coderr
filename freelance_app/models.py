from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from auth_app.models import Profile

class Offer(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='offer/', blank=True, null=True)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.id})"


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

    def __str__(self):
        return f"{self.title} ({self.id})"


class Order(models.Model):
    class Status(models.TextChoices):
        CANCELLED = "cancelled", "Cancelled"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed" ,"Completed"

    customer_user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="customer_user_orders")
    business_user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="business_user_orders")
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, related_name="offer_orders")
    offer_detail = models.ForeignKey(OfferDetail, on_delete=models.SET_NULL, null=True, related_name="offer_detail_orders")
    status = models.CharField(max_length=20, choices=Status.choices, default="in_progress")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.offer_detail.title} ({self.id})"


class Review(models.Model):
    business_user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name="business_user_reviews")
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name="reviewer_reviews")
    rating = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["business_user", "reviewer"],
                name="unique_review_per_reviewer_business_user",
            )
        ]

    def __str__(self):
        return f"{self.reviewer.username} ({self.id})"