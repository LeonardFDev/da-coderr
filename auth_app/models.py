"""Database models for the profile application."""

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """Represents a profile of the application."""

    class Type(models.TextChoices):
        """Defines the possible types of a profile."""
        
        BUSINESS = "business" ,"Business"
        CUSTOMER = "customer", "Customer"
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    type = models.CharField(max_length=20, choices=Type.choices)
    first_name = models.CharField(max_length=100, blank=True, default="")
    last_name = models.CharField(max_length=100, blank=True, default="")
    file = models.ImageField(upload_to='profile/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, default="")
    tel = models.CharField(max_length=20, blank=True, default="")
    description = models.TextField(blank=True, default="")
    working_hours = models.CharField(max_length=100, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]
    
    def __str__(self):
        """Return the username and the id as a string."""
        return f"{self.username} ({self.id})"

    def delete(self, *args, **kwargs):
        """Delete the profile and associated user."""
        user = self.user
        super().delete(*args, **kwargs)
        user.delete()

