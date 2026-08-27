"""Authentication and registration API views."""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .serializers import RegisterSerializer, LoginSerializer


class RegisterView(APIView):
    """Provides an API endpoint for user registration."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Register a new user."""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.instance, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(ObtainAuthToken):
    """Provides an API endpoint for user authentication."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Authenticate the user and return an authentication token, username, email and the user id."""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        token, created = Token.objects.get_or_create(user=data["user"])

        return Response({
            "token": token.key,
            "username": data["username"],
            "email": data["email"],
            "user_id": data["user_id"],
        })
