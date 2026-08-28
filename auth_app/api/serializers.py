"""Serializers for Authentication and registration operations."""

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from auth_app.models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for the User registration and Profile model.

    Provides serialization and validation logic for the User registration and Profile model
    and its REST API representation.
    """

    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    username = serializers.CharField()

    class Meta:
        model = Profile
        fields = ["username","email", "password", "repeated_password", "type"]

    def validate_email(self, value):
        """Validates the value of the ``email`` field."""
        if Profile.objects.filter(email=value).exists():
            raise serializers.ValidationError("email already exists")
        return value

    def validate_username(self, value):
        """Validates the value of the ``username`` field."""
        if Profile.objects.filter(username=value).exists():
            raise serializers.ValidationError("username already exists")
        return value

    def validate(self, value):
        """
        Performs cross-field validation.

        Ensures that ``password`` is equal to ``repeated_password``.
        """
        if value['password'] != value['repeated_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return value

    def create(self, validated_data):
        """
        Creates a new user, profile and generates an authentication token.

        Returns the newly created profile together with the generated token.
        """
        validated_data.pop('repeated_password')
        data = {}

        user = User.objects.create_user(
            username=validated_data['username'],
            email = validated_data["email"],
            password=validated_data['password'],
        )

        token = Token.objects.create(user=user)

        Profile.objects.create(
            user = user,
            username = validated_data["username"],
            email = validated_data["email"],
            type = validated_data["type"]
        )

        data = {
            "token": token.key,
            "username": validated_data["username"],
            "email": validated_data["email"],
            "user_id": user.id
        }

        return data
    
class LoginSerializer(serializers.Serializer):
    """
    Serializer for User authentication. 
    Validates the credentials and uses the authenticated User to output the User's Profile
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validates the user's login credentials.

        Authenticates the user using the provided username and password. 
        Which is then used to output the corresponding profile.
        """
        user = authenticate(
            username=data["username"],
            password=data["password"],
        )

        if user is None:
            raise serializers.ValidationError("Invalid username or password.")

        profile = get_object_or_404(Profile, username = data["username"])

        data["user"] = user
        data["username"] = profile.username
        data["email"] = profile.email
        data["user_id"] = profile.user.id

        return data