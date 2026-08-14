from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from auth_app.models import Profile


class ProfilePermission(BasePermission):
    def has_permission(self, request, view):
        is_authenticated = request.user.is_authenticated
        return is_authenticated

    def has_object_permission(self, request, view, obj):
        is_owner = self.check_owner(request, obj)
        
        if request.method in ("PATCH"):    
            return is_owner
        return True
    
    def check_owner(self, request, profile):
        request_user = request.user
        profile_user = get_object_or_404(Profile, username = request_user)
        is_owner = profile == profile_user

        return is_owner


class OfferPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("POST"):
            is_authenticated = request.user.is_authenticated
            return is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ("POST"):    
            is_type_business  = self.check_type(request)
            return is_type_business

        if request.method in ("PATCH", "DELETE"):
            is_owner = self.check_owner(request, obj)
            return is_owner
        return True
    
    def check_type(self, request):
        request_user = request.user
        is_profile_business = Profile.objects.filter(username = request_user, type = "business").exists()

        return is_profile_business

    def check_owner(self, request, obj):
        request_user = request.user
        profile_user = get_object_or_404(Profile, username = request_user)
        is_owner = obj.user == profile_user
    
        return is_owner

class OrderPermission(BasePermission):
    def has_permission(self, request, view):
        is_authenticated = request.user.is_authenticated

        if request.method == "DELETE":
            return request.user.is_staff
        
        if request.method == "POST":    
            is_type_customer  = self.check_type(request, "customer")
            return is_type_customer
        
        return is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ("PATCH"):
            is_owner = self.check_owner(request, obj)
            is_type_business  = self.check_type(request, "business")
            return is_owner and is_type_business
        return True
    
    def check_type(self, request, typeValue):
        request_user = request.user
        is_profile_business = Profile.objects.filter(username = request_user.username, type = typeValue).exists()

        return is_profile_business

    def check_owner(self, request, obj):
        request_user = request.user
        profile_user = get_object_or_404(Profile, username = request_user)
        is_owner = obj.business_user == profile_user
    
        return is_owner


class ReviewPermission(BasePermission):
    def has_permission(self, request, view):
        is_authenticated = request.user.is_authenticated
        is_customer = self.check_customer(request)

        if request.method in ("POST"):
            return is_customer
        return is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ("PATCH", "DELETE"):
            is_reviewer = self.check_reviewer(request, obj)
            return is_reviewer
    
    def check_customer(self, request):
        request_user = request.user
        profile_user = get_object_or_404(Profile, username = request_user)
        is_customer = profile_user.type == "customer"

        return is_customer

    def check_reviewer(self, request, review):
        request_user = request.user
        profile_user = get_object_or_404(Profile, username = request_user)
        is_reviewer = review.reviewer == profile_user
        
        return is_reviewer