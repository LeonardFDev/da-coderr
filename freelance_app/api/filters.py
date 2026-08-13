import django_filters
from freelance_app.models import Offer, Review


class OfferFilter(django_filters.FilterSet):
    creator_id = django_filters.NumberFilter(
        field_name="user_id",
        lookup_expr="exact"
    )

    min_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="gte"
    )

    max_delivery_time = django_filters.NumberFilter(
        field_name="delivery_time",
        lookup_expr="lte"
    )

    class Meta:
        model = Offer
        fields = []


class ReviewFilter(django_filters.FilterSet):
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
        fields = []