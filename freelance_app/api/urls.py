from django.urls import path, include
from rest_framework import routers

from .views import ProfileDetailView, ProfilesBusinessListView, ProfilesCustomerListView,\
    OfferListView, OfferDetailView, OfferDetailsDetailView, OrderListView, OrderDetailView, \
    OrderCountView, OrderCompletedCountView, ReviewViewSet, BaseInfoListView


router = routers.SimpleRouter()
router.register(r"reviews", ReviewViewSet)

urlpatterns = [
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name = "profile-detail"),
    path("profiles/business/", ProfilesBusinessListView.as_view(), name = "profiles-business-list"),
    path("profiles/customer/", ProfilesCustomerListView.as_view(), name = "profiles-customer-list"),

    path("offers/", OfferListView.as_view(), name = "offer-list"),
    path("offers/<int:id>/", OfferDetailView.as_view(), name = "offer-detail"),
    path("offerdetails/<int:id>/", OfferDetailsDetailView.as_view(), name = "offerdetails-detail"),

    path("orders/", OrderListView.as_view(), name ="order-list"),
    path("orders/<int:id>/", OrderDetailView.as_view(), name ="order-detail"),
    path("order-count/<int:business_user_id>/", OrderCountView.as_view(), name ="order-count-detail"),
    path("completed-order-count/<int:business_user_id>/", OrderCompletedCountView.as_view(), name ="completed-order-count-detail"),

    path("", include(router.urls)),

    path("base-info/", BaseInfoListView.as_view(), name ="base-info-list"),
]

