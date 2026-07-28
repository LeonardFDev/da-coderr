from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    class Type(models.TextChoices):
        BUSINESS = "business" ,"Business"
        CUSTOMER = "customer", "Customer"
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    type = models.CharField(max_length=20, choices=Type.choices)
    first_name = models.CharField(max_length=100, blank=True, default="")
    last_name = models.CharField(max_length=100, blank=True, default="")
    file = models.CharField(max_length=100, blank=True, default="")             # <- aktuell wird bei keiner Eingabe "" gesetzt, vielleicht wird das noch auf Null geändert
    location = models.CharField(max_length=100, blank=True, default="")
    tel = models.CharField(max_length=20, blank=True, default="")
    description = models.CharField(max_length=100, blank=True, default="")
    working_hours = models.CharField(max_length=100, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]
    
    def __str__(self):
        return f"{self.username} ({self.id})"

    def delete(self, *args, **kwargs):
        user = self.user
        super().delete(*args, **kwargs)
        user.delete()

