from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import generics, filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend

from auth_app.models import Profile
from freelance_app.models import Offer, OfferDetail, Order, Review
from .serializers import ProfileSerializer, ProfilesBusinessSerializer, ProfilesCustomerSerializer, \
    OfferCreateSerializer, OfferListSerializer, OfferDetailGetSerializer, OfferDetailsSerializer, \
    OfferDetailPatchSerializer, OrderListSerializer, OrderDetailSerializer, OrderCountSerializer, \
    OrderCompletedCountSerializer, ReviewSerializer
from .permissions import ProfilePermission, OfferPermission, OrderPermission, ReviewPermission
from .pagination import LargeResultsSetPagination
from .filters import OfferFilter, ReviewFilter


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    http_method_names = ["get", "patch"]
    serializer_class = ProfileSerializer
    permission_classes = [ProfilePermission]


class ProfilesBusinessListView(generics.ListAPIView):
    queryset = Profile.objects.filter(type = "business")
    serializer_class = ProfilesBusinessSerializer


class ProfilesCustomerListView(generics.ListAPIView):
    queryset = Profile.objects.filter(type = "customer")
    serializer_class = ProfilesCustomerSerializer


class OfferListView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    permission_classes = [OfferPermission]
    pagination_class = LargeResultsSetPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    filterset_fields = ["creator_id", "min_price", "max_delivery_time"]
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "min_price"]
    ordering = ["id"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OfferCreateSerializer
        return OfferListSerializer

    def perform_create(self, serializer):
        request_username = self.request.user.username
        profile = get_object_or_404(Profile, username = request_username)

        if profile.type != "business":
            raise PermissionDenied("Only users with the type 'business' are allowed to add an offer.")

        serializer.save(user = profile)


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    http_method_names = ["get", "patch", "delete"]
    permission_classes = [OfferPermission]
    lookup_field = "id"

    def get_serializer_class(self):
        if self.request.method == "GET":
            return OfferDetailGetSerializer
        return OfferDetailPatchSerializer


class OfferDetailsDetailView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailsSerializer
    lookup_field = "id"


class OrderListView(generics.ListCreateAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [OrderPermission]

    def get_queryset(self):
        request_username = self.request.user.username
        profile = get_object_or_404(Profile, username = request_username)

        return (Order.objects
            .select_related("offer", "offer_detail")
            .filter(Q(customer_user=profile.id) | Q(business_user=profile.id)))

    def perform_create(self, serializer):
        request_username = self.request.user.username
        profile = get_object_or_404(Profile, username = request_username)
        offer_detail_id = serializer.validated_data["offer_detail_id"]

        offer_detail = OfferDetail.objects.get(id=offer_detail_id)

        serializer.save(customer_user = profile, offer_detail = offer_detail, offer = offer_detail.offer)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    http_method_names = ["patch", "delete"]
    permission_classes = [OrderPermission]
    lookup_field = "id"


class OrderCountView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = OrderCountSerializer
    lookup_url_kwarg = "business_user_id"


class OrderCompletedCountView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = OrderCompletedCountSerializer
    lookup_url_kwarg = "business_user_id"


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewPermission]
    http_method_names = ["get", "post", "patch", "delete"]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReviewFilter
    filterset_fields = ["business_user_id", "reviewer_id"]
    ordering_fields = ["updated_at", "rating"]
    ordering = ["id"]

    def perform_create(self, serializer):
        request_username = self.request.user.username
        profile = get_object_or_404(Profile, username = request_username)
        serializer.save(reviewer=profile)
