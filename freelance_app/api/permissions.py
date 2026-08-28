"""Permission classes for API access control for Profile, Offer, Order, and Review."""

from rest_framework.permissions import BasePermission

from auth_app.models import Profile


class ProfilePermission(BasePermission):
    """Permission for Profile API access."""

    def has_permission(self, request, view):
        is_authenticated = request.user.is_authenticated
        return is_authenticated

    def has_object_permission(self, request, view, obj):
        is_owner = self.check_owner(request, obj)
        
        if request.method in ("PATCH"):    
            return is_owner
        return True
    
    def check_owner(self, request, profile):
        """checks whether the logged in user is the owner of the profile"""
        request_user = request.user
        profile_user = Profile.objects.filter(username = request_user).first()
        is_owner = profile == profile_user

        return is_owner


class OfferPermission(BasePermission):
    """Permission for Offer API access."""

    def has_permission(self, request, view):
        is_authenticated = request.user.is_authenticated

        if request.method in ("GET") and not view.kwargs:
            return True
        
        return is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ("POST"):    
            is_type_business  = self.check_type(request)
            return is_type_business

        if request.method in ("PATCH", "DELETE"):
            is_owner = self.check_owner(request, obj)
            return is_owner
        return True
    
    def check_type(self, request):
        """Checks whether the logged in user has the type Busuness"""
        request_user = request.user
        is_profile_business = Profile.objects.filter(username = request_user, type = "business").exists()

        return is_profile_business

    def check_owner(self, request, obj):
        """checks whether the logged in user is the owner of the Offer"""
        request_user = request.user
        profile_user = Profile.objects.filter(username = request_user).first()
        is_owner = obj.user == profile_user
    
        return is_owner

class OrderPermission(BasePermission):
    """Permission for Order API access."""

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
            is_owner = self.check_business_user(request, obj)
            is_type_business  = self.check_type(request, "business")
            return is_owner and is_type_business
        return True
    
    def check_type(self, request, typeValue):
        """Checks what type the logged-in user is"""
        request_user = request.user
        is_profile_typeValue = Profile.objects.filter(username = request_user.username, type = typeValue).exists()

        return is_profile_typeValue

    def check_business_user(self, request, obj):
        """checks whether the logged in user is the business_user of the Order"""
        request_user = request.user
        profile_user = Profile.objects.filter(username = request_user).first()
        is_owner = obj.business_user == profile_user
    
        return is_owner


class ReviewPermission(BasePermission):
    """Permission for Review API access."""

    def has_permission(self, request, view):
        is_authenticated = request.user.is_authenticated
        is_customer = self.check_customer(request)

        if view.action == "create":
            return is_authenticated and is_customer 
        return is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action in ["partial_update", "destroy"]:
            is_reviewer = self.check_reviewer(request, obj)
            return is_reviewer
    
    def check_customer(self, request):
        """Checks if the logged in user has the type customer"""
        request_user = request.user
        is_customer = Profile.objects.filter(username = request_user, type = "customer").first()

        return is_customer

    def check_reviewer(self, request, review):
        """checks whether the logged in user is the reviewer"""
        request_user = request.user
        profile_user = Profile.objects.filter(username = request_user).first()
        is_reviewer = review.reviewer == profile_user
        
        return is_reviewer