import django_filters
from freelance_app.models import Offer


class OfferFilter(django_filters.FilterSet):
    creator_id = django_filters.NumberFilter(
        field_name="user",
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
