from django.db.models import Min
import django_filters

from freelance_app.models import Offer, Review


class OfferFilter(django_filters.FilterSet):
    creator_id = django_filters.NumberFilter(
        field_name="user_id",
        lookup_expr="exact"
    )

    max_delivery_time = django_filters.NumberFilter(
        field_name= "offer_details__delivery_time_in_days",
        lookup_expr="lte"
    )

    min_price = django_filters.NumberFilter(
        method="filter_min_price"
    )

    class Meta:
        model = Offer
        fields = ["creator_id", "max_delivery_time", "min_price"]

    def filter_min_price(self, queryset, name, value):
        return queryset.annotate(min_price=Min("offer_details__price")).filter(min_price__gte=value)


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