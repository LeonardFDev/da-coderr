from django.db.models import Min
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.exceptions import PermissionDenied, NotFound

from auth_app.models import Profile
from freelance_app.models import Offer, OfferDetail


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


class OfferUserDetails(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "username"]


class OfferDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        exclude = ["offer"]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        price = float(instance.price)

        if price.is_integer():
            data["price"] = int(price)
        else:
            data["price"] = price

        return data


class OfferDetailsPartPathSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"


class OfferDetailsCompletePathListSerializer(serializers.HyperlinkedModelSerializer):  #noch nicht verwändet (ist das mit dem vollständigen Pfad)
    class Meta:
        model = OfferDetail
        fields = ["id", "url"]


class OfferCreateSerializer(serializers.ModelSerializer):
    details = OfferDetailsSerializer(many=True, source="offer_details")

    class Meta:
        model = Offer
        fields = fields = ["id", "title", "image", "description", "details"]
        read_only_fields = ["user"]

    def get_min_price(self, obj):
        return float(obj.offer_details.aggregate(min_price=Min("price"))["min_price"])

    def get_min_delivery_time(self, obj):
        return obj.offer_details.aggregate(min_delivery_time=Min("delivery_time_in_days"))["min_delivery_time"]

    def create(self, validated_data):
        offer_details_data = validated_data.pop("offer_details")

        offer = Offer.objects.create(**validated_data)

        for offer_detail_data in offer_details_data:
            OfferDetail.objects.create(offer=offer, **offer_detail_data)
        return offer


class OfferListSerializer(serializers.ModelSerializer):
    details = OfferDetailsPartPathSerializer(many=True, source="offer_details")
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = OfferUserDetails(source = "user")

    class Meta:
        model = Offer
        fields = ["id", "user", "title", "image", "description", "created_at", "updated_at", "details", "min_price", "min_delivery_time", "user_details"]

    def get_min_price(self, obj):
        price = float(obj.offer_details.aggregate(min_price=Min("price"))["min_price"])

        if price.is_integer():
            return int(price)
        else:
            return price
    
    def get_min_delivery_time(self, obj):
        return obj.offer_details.aggregate(min_delivery_time=Min("delivery_time_in_days"))["min_delivery_time"]