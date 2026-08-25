from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "type", "fullname", "email", "user_id")
    ordering = ["id"]
    search_fields = ("username", "first_name", "last_name")

    @admin.display(description="Name")
    def fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}"