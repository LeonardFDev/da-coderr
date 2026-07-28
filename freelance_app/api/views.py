from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied

from auth_app.models import Profile
from .serializers import ProfileSerializer, ProfilesBusinessSerializer, ProfilesCustomerSerializer
from .permissions import IsOwnerPatch


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    http_method_names = ["get", "patch"]
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerPatch]


class ProfilesBusinessListView(generics.ListAPIView):
    queryset = Profile.objects.filter(type = "business")
    serializer_class = ProfilesBusinessSerializer


class ProfilesCustomerListView(generics.ListAPIView):
    queryset = Profile.objects.filter(type = "customer")
    serializer_class = ProfilesCustomerSerializer