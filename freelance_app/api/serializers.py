"""Serializers for Profile, Offer, Offer Detail, Order and Review API operations."""

from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db.models import Min
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from auth_app.models import Profile
from freelance_app.models import Offer, OfferDetail, Order, Review


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for the Profile model."""

    class Meta:
        model = Profile
        fields = ["user", "username", "first_name", "last_name", "file", "location", "tel", "description", "working_hours", "type", "email", "created_at"]


class ProfilesBusinessSerializer(serializers.ModelSerializer):
    """Serializer for the Profile model with the type business."""

    class Meta:
        model = Profile
        fields = ["user", "username", "first_name", "last_name", "file", "location", "tel", "description", "working_hours", "type"]


class ProfilesCustomerSerializer(serializers.ModelSerializer):
    """Serializer for the Profile model with the type customer."""

    class Meta:
        model = Profile
        fields = ["user", "username", "first_name", "last_name", "file", "uploaded_at", "type"]


class OfferUserDetails(serializers.ModelSerializer):
    """Nested serializer for the Profile model in OfferListSerializer."""

    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "username"]


class OfferDetailsSerializer(serializers.ModelSerializer):
    """Nested serializer for the OfferDetail model in OfferCreateSerializer and OfferDetailPatchSerializer."""

    class Meta:
        model = OfferDetail
        exclude = ["offer"]
        read_only_fields = ["id"]

    def to_representation(self, instance):
        """Output the price as a decimal value, as an integer or float"""

        data = super().to_representation(instance)

        price = float(instance.price)

        if price.is_integer():
            data["price"] = int(price)
        else:
            data["price"] = price

        return data


class OfferDetailsListCompletePathListSerializer(serializers.HyperlinkedModelSerializer):
    """Nested serializer for the OfferDetail model in OfferDetailGetSerializer."""

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]

        extra_kwargs = {
            "url": {
                "view_name": "offerdetails-detail",
                "lookup_field": "id",
            }
        }


class OfferDetailsListPartPathSerializer(serializers.ModelSerializer):
    """Nested serializer for the OfferDetail model in OfferListSerializer."""

    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]

    def get_url(self, obj):
        """the URL is taken and only part of the URL is output."""
        url = reverse("offerdetails-detail", kwargs={"id": obj.pk})
        API_PREFIX = "/api"
        url_without_api = url.replace(API_PREFIX, "", 1)
        return url_without_api


class OfferListSerializer(serializers.ModelSerializer):
    """
    Base serializer for OfferCreateSerializer and OfferDetailGetSerializer.

    Provides common serialization and validation logic.
    """

    details = OfferDetailsListPartPathSerializer(many=True, source="offer_details")
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = OfferUserDetails(source = "user")

    class Meta:
        model = Offer
        fields = ["id", "user", "title", "image", "description", "created_at", "updated_at", "details", "min_price", "min_delivery_time", "user_details"]

    def get_min_price(self, obj):
        """Searches for the lowest price and outputs that decimal value as a whole integer or float"""
        min_price = float(obj.offer_details.aggregate(min_price=Min("price"))["min_price"])

        if min_price.is_integer():
            return int(min_price)
        else:
            return min_price
    
    def get_min_delivery_time(self, obj):
        """Searches for the lowest delivery time and outputs that"""
        return obj.offer_details.aggregate(min_delivery_time=Min("delivery_time_in_days"))["min_delivery_time"]


class OfferCreateSerializer(OfferListSerializer, serializers.ModelSerializer):
    """Serializer for creating Offer instances via POST requests"""

    details = OfferDetailsSerializer(many=True, source="offer_details")

    class Meta:
        model = Offer
        fields = fields = ["id", "title", "image", "description", "details"]
        read_only_fields = ["user"]

    def validate_details(self, value):
        """Validates the "details" field and checks if there are exactly 3 objects."""
        if len(value) != 3:
            raise serializers.ValidationError("Exactly 3 details objects must be specified.")
        
        offer_type_values = [offer_detail["offer_type"] for offer_detail in value]
        if len(offer_type_values) != len(set(offer_type_values)):
            raise serializers.ValidationError("basic, standard and premium allowed to occur only once and must not appear multiple times.")
        return value

    def create(self, validated_data):
        """Creates a new offer and three offer details instance from the validated data."""
        offer_details_data = validated_data.pop("offer_details")

        offer = Offer.objects.create(**validated_data)

        for offer_detail_data in offer_details_data:
            OfferDetail.objects.create(offer=offer, **offer_detail_data)
        return offer


class OfferDetailGetSerializer(OfferListSerializer, serializers.ModelSerializer):
    """Serializer for detailed Offer data."""

    details = OfferDetailsListCompletePathListSerializer(many=True, source="offer_details")

    class Meta:
        model = Offer
        fields = ["id", "user", "title", "image", "description", "created_at", "updated_at", "details", "min_price", "min_delivery_time"]


class OfferDetailPatchSerializer(serializers.ModelSerializer):
    """Serializer for updating Offer details via PATCH requests."""

    details = OfferDetailsSerializer(many=True, source="offer_details")

    class Meta:
        model = Offer
        fields = ["id", "title", "image", "description", "details"]
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
        """Updates the offer and the three offer details instance with the validated data."""
        changed_offer_details_data = []

        offer_details_data = validated_data.pop("offer_details", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        self.check_offer_details_data(instance, offer_details_data, changed_offer_details_data)

        for offer_detail_data in changed_offer_details_data:
            offer_detail_data.save()
        return instance

    def check_offer_details_data(self, instance, offer_details_data, changed_offer_details_data):
        """Checks if the values fit in offer_details, otherwise there is a validation error"""
        self.multiple_offer_type(offer_details_data)

        existing_offer_details = {
            offer_detail.offer_type: offer_detail
            for offer_detail in instance.offer_details.all()
        }

        self.ensure_values_are_present_and_valid(offer_details_data, existing_offer_details, changed_offer_details_data)

    def multiple_offer_type(self, offer_details_data):
        """Check if the three offer_type are different and otherwise give a validation error"""
        offer_type_list = [
            offer_detail_data.get("offer_type")
            for offer_detail_data in offer_details_data
        ]

        multiple = {
            offer_type_single for offer_type_single in offer_type_list
            if offer_type_list.count(offer_type_single) > 1
        }

        if multiple:
            raise serializers.ValidationError({"details": f"multiple offer_type value: {multiple}"})

    def ensure_values_are_present_and_valid(self, offer_details_data, existing_offer_details, changed_offer_details_data):
        """Checks whether the offer_type value exists and is allowed"""
        for offer_detail_data in offer_details_data:
            offer_type_value = offer_detail_data.get("offer_type")
            self.no_offer_type_values(offer_type_value)
            offer_detail = existing_offer_details.get(offer_type_value)
            self.offer_type_does_not_exist(offer_detail, offer_type_value)
            offer_detail_data.pop("offer_type", None)

            for attr, value in offer_detail_data.items():
                setattr(offer_detail, attr, value)
            changed_offer_details_data.append(offer_detail)

    def no_offer_type_values(self, offer_type_value):
        """Check if offer_type is specified, otherwise it will result in a validation error"""
        if not offer_type_value:
            raise serializers.ValidationError(
                {"details": "offer_type is needed in every single detail"}
            )

    def offer_type_does_not_exist(self, offer_detail, offer_type_value):
        """Check if the offer_type you entered is allowed, otherwise it will result in a validation error"""
        if offer_detail is None:
            raise serializers.ValidationError({"details": f"the offer_type '{offer_type_value}' doesn't exist."})


class OrderListSerializer(serializers.ModelSerializer):
    """Base serializer for listing Order instances. Used by OrderDetailSerializer."""

    offer_detail_id = serializers.IntegerField(write_only=True)
    business_user = serializers.PrimaryKeyRelatedField(source="offer_detail.offer.user", read_only=True)
    title = serializers.CharField(source="offer_detail.title", read_only=True)
    revisions = serializers.IntegerField(source="offer_detail.revisions", read_only=True)
    delivery_time_in_days = serializers.IntegerField(source="offer_detail.delivery_time_in_days", read_only=True)
    price = serializers.DecimalField(source="offer_detail.price", max_digits=10, decimal_places=2, coerce_to_string=False, read_only=True)
    features = serializers.JSONField(source="offer_detail.features", read_only=True)
    offer_type = serializers.CharField(source="offer_detail.offer_type", read_only=True)
    
    class Meta:
        model = Order
        fields = [
            "offer_detail_id", "id", "customer_user", "business_user", "title", 
            "revisions", "delivery_time_in_days", "price", "features", "offer_type", 
            "status", "created_at", "updated_at"]
        read_only_fields = ["id", "customer_user", "created_at", "updated_at", "status"]

    def validate_offer_detail_id(self, id):
        """Validates the ``offer_detail_id`` field. Ensures that the referenced offer_detail instance exists."""
        try:
            OfferDetail.objects.get(id=id)
        except OfferDetail.DoesNotExist:
            raise NotFound(
                f"Invalid pk \"{id}\" - object does not exist."
            )

        return id


class OrderDetailSerializer(OrderListSerializer, serializers.ModelSerializer):
    """Serializer for detailed Order data."""

    class Meta:
        model = Order
        fields = [
            "id", "customer_user", "business_user", "title", 
            "revisions", "delivery_time_in_days", "price", "features", 
            "offer_type","status", "created_at", "updated_at"]
        read_only_fields = [
            "id", "customer_user", "business_user", "title", 
            "revisions", "delivery_time_in_days", "price", "features", 
            "offer_type", "created_at", "updated_at"]

    def validate(self, attrs):
        """Validates that ``status`` is present."""
        if self.instance and "status" not in attrs:
            raise serializers.ValidationError({
                "status": "This field is required."
            })
        return attrs


class OrderCountSerializer(serializers.ModelSerializer):
    """Serializer for the output of aggregated purchase orders with status in progress"""

    order_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["order_count"]

    def get_order_count(self, obj):
        """Count the orders that are the status in progress"""
        return obj.business_user_orders.filter(status = "in_progress").count()


class OrderCompletedCountSerializer(serializers.ModelSerializer):
    """Serializer for the output of aggregated purchase orders with status completed"""

    completed_order_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["completed_order_count"]

    def get_completed_order_count(self, obj):
        """Count the orders that are the status completed"""
        return obj.business_user_orders.filter(status = "completed").count()


class ReviewSerializer(serializers.ModelSerializer):
    """    Base serializer for the Review model, used by ReviewPatchSerializer."""

    class Meta:
        model = Review
        fields = ["id", "business_user", "reviewer", "rating", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "reviewer", "created_at", "updated_at"]

    def validate_business_user(self, business_user):
        """Checks whether the user has already submitted a review"""
        request_username = self.context["request"].user.username
        reviewer = get_object_or_404(Profile, username = request_username)

        if Review.objects.filter(business_user=business_user, reviewer=reviewer,).exists():
            raise serializers.ValidationError("You have already rated this User.")
        return business_user


class ReviewPatchSerializer(ReviewSerializer, serializers.ModelSerializer):
    """Serializer for updating Review instances via PATCH requests."""

    class Meta:
        model = Review
        fields = ["id", "business_user", "reviewer", "rating", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "business_user", "reviewer", "created_at", "updated_at"]