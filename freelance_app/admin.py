"""Admin configurations for Offer, Offer deatil, Order, Review"""

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html_join
from django.utils.html import format_html
from .models import Offer, OfferDetail, Order, Review


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """Admin configuration for the Offer model."""

    list_display = ("id", "title", "description", "user", "offer_details")
    ordering = ["id"]
    search_fields = ("title", "description", "user__username", "offer_details__title")

    @admin.display(description="Details")
    def offer_details(self, obj):
        """Returns the details as a link displayed in the admin list."""
        def offer_deails_link(offer_details):
            """Generate the URL and pass the URL, the Offer Details Title, and the Offer Details ID"""
            url = reverse("admin:freelance_app_offerdetail_change", args=[offer_details.id])
            return url, offer_details.title, offer_details.id

        return format_html_join(", ", "[<a href='{}''>{} ({})</a>]",
            (offer_deails_link(offer_details) for offer_details in obj.offer_details.all().order_by("id"))
        )
    

@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
    """Admin configuration for the Offer detail model."""

    list_display = ("id", "title", "price", "custom_offer")
    ordering = ["id"]
    search_fields = ("title", "offer__title")

    @admin.display(description="Offer")
    def custom_offer(self, obj):
        """Returns the offer as a link displayed in the admin list."""
        offer = obj.offer
        url = reverse("admin:freelance_app_offer_change", args=[offer.id])
        path = "<a href='{}'>{} ({})</a>"
    
        return format_html(path, url, offer.title, offer.id)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for the Order model."""

    list_display = ("id", "customer_user", "business_user", "offer_detail")
    ordering = ["id"]
    search_fields = ("customer_user__username", "business_user__username", "offer_detail__title")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin configuration for the Review model."""
    
    list_display = ("id", "reviewer", "business_user", "rating")
    ordering = ["id"]
    search_fields = ("reviewer__username", "business_user__username")