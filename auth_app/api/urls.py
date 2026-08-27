"""URL configuration for the authentication and registration API."""

from django.urls import path

from .views import RegisterView, LoginView

urlpatterns = [
    path("registration/", RegisterView.as_view(), name = "registration"),
    path("login/", LoginView.as_view(), name = "login"),
]