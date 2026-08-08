from django.urls import path

from .views import ProfileDetailView, ProfilesBusinessListView, ProfilesCustomerListView,\
    OfferListView, OfferDetailView, OfferDetailsDetailView, OrderListView

urlpatterns = [
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name = "profile-detail"),
    path("profiles/business/", ProfilesBusinessListView.as_view(), name = "profiles-business-list"),
    path("profiles/customer/", ProfilesCustomerListView.as_view(), name = "profiles-customer-list"),

    path("offers/", OfferListView.as_view(), name = "offer-list"),
    path("offers/<int:id>/", OfferDetailView.as_view(), name = "offer-detail"),
    path("offerdetails/<int:id>/", OfferDetailsDetailView.as_view(), name = "offerdetails-detail"),

    path("api/orders/", OrderListView.as_view(), name ="order-list")
    # path("api/orders/<int:id>/", .as_view(), name ="order-detail")
    # path("api/order-count/<int:business_user_id>/", .as_view(), name ="order-count-list")
    # path("api/completed-order-count/<int:business_user_id>/", .as_view(), name ="completed-order-count-list")
]

