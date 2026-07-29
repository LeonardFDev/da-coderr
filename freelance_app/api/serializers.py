from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.exceptions import PermissionDenied, NotFound

from auth_app.models import Profile
from freelance_app.models import Offer


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["user", "username", "first_name", "last_name", "file", "location", "tel", "description", "working_hours", "type", "email", "created_at"]


class ProfilesBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["user", "username", "first_name", "last_name", "file", "location", "tel", "description", "working_hours", "type"]


class ProfilesCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["user", "username", "first_name", "last_name", "file", "uploaded_at", "type"]


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ["id", "user", "title", "image", "description", "detail"]