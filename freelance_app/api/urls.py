from django.urls import path

from .views import ProfileDetailView, ProfilesBusinessListView, ProfilesCustomerListView

urlpatterns = [
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name = "profile-deatil"),
    path("profiles/business/", ProfilesBusinessListView.as_view(), name = "profiles-business-list"),
    path("profiles/customer/", ProfilesCustomerListView.as_view(), name = "profiles-customer-list"),
]