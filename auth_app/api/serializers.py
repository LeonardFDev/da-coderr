from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from auth_app.models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    username = serializers.CharField()


    class Meta:
        model = Profile
        fields = ["username","email", "password", "repeated_password", "type"]

    def validate_email(self, value):
        if Profile.objects.filter(email=value).exists():
            raise serializers.ValidationError("email already exists")
        return value

    def validate_username(self, value):
        if Profile.objects.filter(username=value).exists():
            raise serializers.ValidationError("username already exists")
        return value

    def validate(self, value):
        if value['password'] != value['repeated_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return value

    def create(self, validated_data):
        validated_data.pop('repeated_password')
        data = {}

        user = User.objects.create_user(
            username=validated_data['email'],
            password=validated_data['password']
        )

        token = Token.objects.create(user=user)

        Profile.objects.create(
            user = user,
            username = validated_data["username"],
            email = validated_data["email"],
        )

        data = {
            "token": token.key,
            "username": validated_data["username"],
            "email": validated_data["email"],
            "user_id": user.id
        }

        return data
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
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