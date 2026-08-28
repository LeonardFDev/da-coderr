"""
Filters for API query parameters.

Contains filters for filtering API data based on query parameters.
"""

from django.db.models import Min
import django_filters

from freelance_app.models import Offer, Review


class OfferFilter(django_filters.FilterSet):
    """Filter for Offer query parameters."""

    creator_id = django_filters.NumberFilter(
        field_name="user_id",
        lookup_expr="exact"
    )

    max_delivery_time = django_filters.NumberFilter(
        method="filter_max_delivery_time"
    )

    min_price = django_filters.NumberFilter(
        method="filter_min_price"
    )

    class Meta:
        model = Offer
        fields = ["creator_id", "max_delivery_time", "min_price"]

    def filter_max_delivery_time(self, queryset, name, value):
        """Filters the queryset based on ``max_delivery_time``."""
        return queryset.annotate(max_delivery_time=Min("offer_details__delivery_time_in_days")).filter(max_delivery_time__lte=value)
    
    def filter_min_price(self, queryset, name, value):
        """Filters the queryset based on ``min_price``."""
        return queryset.annotate(min_price=Min("offer_details__price")).filter(min_price__gte=value)


class ReviewFilter(django_filters.FilterSet):
    """Filter for Review query parameters."""

    business_user_id = django_filters.NumberFilter(
        field_name="business_user_id",
        lookup_expr="exact",
    )

    reviewer_id = django_filters.NumberFilter(
        field_name="reviewer_id",
        lookup_expr="exact",
    )

    class Meta:
        model = Review
        fields = ["business_user_id", "reviewer_id"]