from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from auth_app.models import Profile


class ProfileDetailPermission(BasePermission):
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


class OfferListPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("POST"):
            is_authenticated = request.user.is_authenticated
            return is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ("POST"):    
            is_type_business  = self.check_type(request)
            return is_type_business
        return True
    
    def check_type(self, request):
        request_user = request.user
        is_profile_business = Profile.objects.filter(username = request_user, type = "business").exists()

        return is_profile_business














#     def checkMembers(self, request, board):
#         email = request.user.username
#         user = get_object_or_404(KanMindUser, email = email)
#         is_member = board.members.filter(id = user.id).exists()

#         return is_member

# class IsOwnerOrMemberTask(BasePermission):
#     def has_permission(self, request, view):
#         is_authenticated = request.user.is_authenticated
#         return is_authenticated
    
#     def has_object_permission(self, request, view, obj):
#         is_owner = self.checkOwner(request, obj)
#         is_member = self.checkMembers(request, obj)
        
#         if request.method in ("POST", "PATCH"):    
#             return is_member
        
#         if(request.method == "DELETE"):
#             return is_owner | is_member
    
#     def checkOwner(self, request, task):
#         email = request.user.username
#         user = get_object_or_404(KanMindUser, email = email)
#         is_owner = task.board.owner == user

#         return is_owner
    
#     def checkMembers(self, request, task):
#         email = request.user.username
#         user = get_object_or_404(KanMindUser, email = email)
#         is_member = task.board.members.filter(id = user.id).exists()

#         return is_member
    
# class IsCommentCreator(BasePermission):
#     def has_permission(self, request, view):
#         is_authenticated = request.user.is_authenticated
#         return is_authenticated
    
#     def has_object_permission(self, request, view, obj):
#         is_comment_creator = self.checkCommentCreator(request, obj)
        
#         if(request.method == "DELETE"):
#             return is_comment_creator
    
#     def checkCommentCreator(self, request, comment):
#         email = request.user.username
#         user = get_object_or_404(KanMindUser, email = email)
#         is_comment_creator = comment.author == user

#         return is_comment_creator
    