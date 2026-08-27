from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db.models import Min
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from auth_app.models import Profile
from freelance_app.models import Offer, OfferDetail, Order, Review


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
        read_only_fields = ["id"]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        price = float(instance.price)

        if price.is_integer():
            data["price"] = int(price)
        else:
            data["price"] = price

        return data


class OfferDetailsListCompletePathListSerializer(serializers.HyperlinkedModelSerializer):
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
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]

    def get_url(self, obj):
        url = reverse("offerdetails-detail", kwargs={"id": obj.pk})
        API_PREFIX = "/api"
        url_without_api = url.replace(API_PREFIX, "", 1)
        return url_without_api


class OfferListSerializer(serializers.ModelSerializer):
    details = OfferDetailsListPartPathSerializer(many=True, source="offer_details")
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = OfferUserDetails(source = "user")

    class Meta:
        model = Offer
        fields = ["id", "user", "title", "image", "description", "created_at", "updated_at", "details", "min_price", "min_delivery_time", "user_details"]

    def get_min_price(self, obj):
        min_price = float(obj.offer_details.aggregate(min_price=Min("price"))["min_price"])

        if min_price.is_integer():
            return int(min_price)
        else:
            return min_price
    
    def get_min_delivery_time(self, obj):
        return obj.offer_details.aggregate(min_delivery_time=Min("delivery_time_in_days"))["min_delivery_time"]


class OfferCreateSerializer(OfferListSerializer, serializers.ModelSerializer):
    details = OfferDetailsSerializer(many=True, source="offer_details")

    class Meta:
        model = Offer
        fields = fields = ["id", "title", "image", "description", "details"]
        read_only_fields = ["user"]

    def validate_details(self, value):
        if len(value) != 3:
            raise serializers.ValidationError("Exactly 3 details objects must be specified.")
        
        offer_type_values = [offer_detail["offer_type"] for offer_detail in value]
        if len(offer_type_values) != len(set(offer_type_values)):
            raise serializers.ValidationError("basic, standard and premium allowed to occur only once and must not appear multiple times.")
        return value

    def create(self, validated_data):
        offer_details_data = validated_data.pop("offer_details")

        offer = Offer.objects.create(**validated_data)

        for offer_detail_data in offer_details_data:
            OfferDetail.objects.create(offer=offer, **offer_detail_data)
        return offer


class OfferDetailGetSerializer(OfferListSerializer, serializers.ModelSerializer):
    details = OfferDetailsListCompletePathListSerializer(many=True, source="offer_details")

    class Meta:
        model = Offer
        fields = ["id", "user", "title", "image", "description", "created_at", "updated_at", "details", "min_price", "min_delivery_time"]


class OfferDetailPatchSerializer(serializers.ModelSerializer):
    details = OfferDetailsSerializer(many=True, source="offer_details")

    class Meta:
        model = Offer
        fields = ["id", "title", "image", "description", "details"]
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
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
        self.multiple_offer_type(offer_details_data)

        existing_offer_details = {
            offer_detail.offer_type: offer_detail
            for offer_detail in instance.offer_details.all()
        }

        self.ensure_values_are_present_and_valid(offer_details_data, existing_offer_details, changed_offer_details_data)

    def multiple_offer_type(self, offer_details_data):
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
        if not offer_type_value:
            raise serializers.ValidationError(
                {"details": "offer_type is needed in every single detail"}
            )

    def offer_type_does_not_exist(self, offer_detail, offer_type_value):
        if offer_detail is None:
            raise serializers.ValidationError({"details": f"the offer_type '{offer_type_value}' doesn't exist."})


class OrderListSerializer(serializers.ModelSerializer):
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
        try:
            OfferDetail.objects.get(id=id)
        except OfferDetail.DoesNotExist:
            raise NotFound(
                f"Invalid pk \"{id}\" - object does not exist."
            )

        return id


class OrderDetailSerializer(OrderListSerializer, serializers.ModelSerializer):
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
        if self.instance and "status" not in attrs:
            raise serializers.ValidationError({
                "status": "This field is required."
            })
        return attrs


class OrderCountSerializer(serializers.ModelSerializer):
    order_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["order_count"]

    def get_order_count(self, obj):
        return obj.business_user_orders.filter(status = "in_progress").count()


class OrderCompletedCountSerializer(serializers.ModelSerializer):
    completed_order_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["completed_order_count"]

    def get_completed_order_count(self, obj):
        return obj.business_user_orders.filter(status = "completed").count()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "business_user", "reviewer", "rating", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "reviewer", "created_at", "updated_at"]

    def validate_business_user(self, business_user):
        request_username = self.context["request"].user.username
        reviewer = get_object_or_404(Profile, username = request_username)

        if Review.objects.filter(business_user=business_user, reviewer=reviewer,).exists():
            raise serializers.ValidationError("You have already rated this User.")
        return business_user


class ReviewPatchSerializer(ReviewSerializer, serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "business_user", "reviewer", "rating", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "business_user", "reviewer", "created_at", "updated_at"]