from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from auth_app.models import Profile
from freelance_app.models import Offer
from .serializers import ProfileSerializer, ProfilesBusinessSerializer, ProfilesCustomerSerializer, OfferSerializer
from .permissions import ProfileDetailPermission, OfferListPermission
from .pagination import LargeResultsSetPagination


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    http_method_names = ["get", "patch"]
    serializer_class = ProfileSerializer
    permission_classes = [ProfileDetailPermission]


class ProfilesBusinessListView(generics.ListAPIView):
    queryset = Profile.objects.filter(type = "business")
    serializer_class = ProfilesBusinessSerializer


class ProfilesCustomerListView(generics.ListAPIView):
    queryset = Profile.objects.filter(type = "customer")
    serializer_class = ProfilesCustomerSerializer


class OfferListView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [OfferListPermission]
    pagination_class = LargeResultsSetPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["author__username"]
    search_fields = ["content"]
    ordering_fields = ["content", "author__username"]
    ordering = ["content"]





# creator_id	                     integer	Filtert die Angebote nach dem Benutzer, der sie erstellt hat.
# min_price	float	                            Filtert Angebote mit einem Mindestpreis.
# max_delivery_time	                 integer	Filtert Angebote, deren Lieferzeit kürzer oder gleich dem angegebenen Wert ist.
# ordering	                         string	    Sortiert die Angebote nach den Feldern 'updated_at' oder 'min_price'.
# search	                         string	    Durchsucht die Felder 'title' und 'description' nach Übereinstimmungen.
# page_size	                         integer	Gibt an, wie viele Ergebnisse pro Seite zurückgegeben werden sollen. Dies sollte mit dem Frontend abgestimmt sein.