"""Profiles, offers, offer detils, orders, review and base info API views."""

from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg, Min
from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from auth_app.models import Profile
from freelance_app.models import Offer, OfferDetail, Order, Review
from .serializers import ProfileSerializer, ProfilesBusinessSerializer, ProfilesCustomerSerializer, \
    OfferCreateSerializer, OfferListSerializer, OfferDetailGetSerializer, OfferDetailsSerializer, \
    OfferDetailPatchSerializer, OrderListSerializer, OrderDetailSerializer, OrderCountSerializer, \
    OrderCompletedCountSerializer, ReviewSerializer, ReviewPatchSerializer
from .permissions import ProfilePermission, OfferPermission, OrderPermission, ReviewPermission
from .pagination import LargeResultsSetPagination
from .filters import OfferFilter, ReviewFilter


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """Provides an API endpoint for retrieving and updating a profile."""

    queryset = Profile.objects.all()
    http_method_names = ["get", "patch"]
    serializer_class = ProfileSerializer
    permission_classes = [ProfilePermission]


class ProfilesBusinessListView(generics.ListAPIView):
    """Provides an API endpoint for listing profiles where the type is business."""
    
    queryset = Profile.objects.filter(type = "business")
    serializer_class = ProfilesBusinessSerializer


class ProfilesCustomerListView(generics.ListAPIView):
    """Provides an API endpoint for listing profiles where the type is customer."""

    queryset = Profile.objects.filter(type = "customer")
    serializer_class = ProfilesCustomerSerializer


class OfferListView(generics.ListCreateAPIView):
    """Provides an API endpoint for listing and creating offers."""

    queryset = Offer.objects.all()
    permission_classes = [OfferPermission]
    pagination_class = LargeResultsSetPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "min_price"]
    ordering = ["id"]

    def get_queryset(self):
        """Return offers ordered by 'id', 'updated_at' or 'min_price'."""
        queryset = Offer.objects.all()

        ordering = self.request.query_params.get("ordering", "")

        if "min_price" in ordering:
            queryset = Offer.objects.annotate(min_price=Min("offer_details__price"))
        return queryset

    def get_serializer_class(self):
        """Return the appropriate serializer for the current request."""
        if self.request.method == "POST":
            return OfferCreateSerializer
        return OfferListSerializer

    def perform_create(self, serializer):
        """Create a offer and hands over the logged in user."""
        request_username = self.request.user.username
        profile = get_object_or_404(Profile, username = request_username)

        if profile.type != "business":
            raise PermissionDenied("Only users with the type 'business' are allowed to add an offer.")

        serializer.save(user = profile)


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Provides an API endpoint for retrieving, updating, and deleting offer details."""

    queryset = Offer.objects.all()
    http_method_names = ["get", "patch", "delete"]
    permission_classes = [OfferPermission]
    lookup_field = "id"

    def get_serializer_class(self):
        """Return the appropriate serializer for the current request."""
        if self.request.method == "GET":
            return OfferDetailGetSerializer
        return OfferDetailPatchSerializer


class OfferDetailsDetailView(generics.RetrieveAPIView):
    """Provides an API endpoint for retrieving an offer details."""

    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailsSerializer
    lookup_field = "id"


class OrderListView(generics.ListCreateAPIView):
    """Provides an API endpoint for listing and creating orders."""

    serializer_class = OrderListSerializer
    permission_classes = [OrderPermission]

    def get_queryset(self):
        """Returns the orders associated with the logged-in user, either as a customer or as a business partner."""
        request_username = self.request.user.username
        profile = get_object_or_404(Profile, username = request_username)

        return (Order.objects
            .select_related("offer", "offer_detail")
            .filter(Q(customer_user=profile.id) | Q(business_user=profile.id)))

    def perform_create(self, serializer):
        """Create a order and hands over the logged in user.
        In addition, the submitted ID is used to pass the business user, offer detail and offer"""
        request_username = self.request.user.username
        profile = get_object_or_404(Profile, username = request_username)
        offer_detail_id = serializer.validated_data["offer_detail_id"]

        offer_detail = OfferDetail.objects.get(id=offer_detail_id)

        serializer.save(customer_user = profile, business_user = offer_detail.offer.user, offer_detail = offer_detail, offer = offer_detail.offer)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Provides an API endpoint for retrieving, updating, and deleting order."""

    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    http_method_names = ["patch", "delete"]
    permission_classes = [OrderPermission]
    lookup_field = "id"


class OrderCountView(generics.RetrieveAPIView):
    """Provides an endpoint returns the number of orders in progress from a given business user."""

    queryset = Profile.objects.all()
    serializer_class = OrderCountSerializer
    lookup_url_kwarg = "business_user_id"


class OrderCompletedCountView(generics.RetrieveAPIView):
    """Provides an endpoint returns the number of orders in completed from a given business user."""

    queryset = Profile.objects.all()
    serializer_class = OrderCompletedCountSerializer
    lookup_url_kwarg = "business_user_id"


class ReviewViewSet(ModelViewSet):
    """Provides API endpoints for managing reviews."""

    queryset = Review.objects.all()
    permission_classes = [ReviewPermission]
    http_method_names = ["get", "post", "patch", "delete"]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReviewFilter
    filterset_fields = ["business_user_id", "reviewer_id"]
    ordering_fields = ["updated_at", "rating"]
    ordering = ["id"]

    def get_serializer_class(self):
        """Return the appropriate serializer for the current action."""
        if self.request.method == "PATCH":
            return ReviewPatchSerializer
        return ReviewSerializer
    
    def perform_create(self, serializer):
        """Create a review and hands over the logged in user."""
        request_username = self.request.user.username
        profile = get_object_or_404(Profile, username = request_username)
        serializer.save(reviewer=profile)

class BaseInfoListView(APIView):
    """Provides an API endpoint for retrieving base info"""

    permission_classes = [AllowAny]

    def get(self, request):
        """Return a list with review count, average rating, business profile count and offer count."""
        review_count = Review.objects.count()
        average_rating = Review.objects.aggregate(Avg("rating"))["rating__avg"]
        average_rating = self.check_average_rating_value(average_rating)
        business_profile_count = Profile.objects.filter(type = "business").count()
        offer_count = Offer.objects.count()

        return Response({
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count,
        })

    def check_average_rating_value(self, average_rating):
        """Checks if there is a value and returns it rounded to one decimal place, if there is no value, a "-" is returned"""
        if average_rating != None:
            return round(average_rating, 1)
        else:
            return "-"
