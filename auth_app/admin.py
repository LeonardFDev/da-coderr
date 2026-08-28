"""Django admin configurations."""

from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin configuration for the Profile model."""

    list_display = ("id", "username", "type", "fullname", "email", "user_id")
    ordering = ["id"]
    search_fields = ("username", "first_name", "last_name")

    @admin.display(description="Name")
    def fullname(self, obj):
        """Returns the fullname displayed in the admin list."""
        return f"{obj.first_name} {obj.last_name}"