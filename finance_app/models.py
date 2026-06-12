import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

# --- NEW: Custom Tags Table ---
class CustomTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tag_type = models.CharField(max_length=50) # Will store either 'category' or 'payment_method'
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.tag_type})"

# --- UPDATED: Expense Table ---
class Expense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField() # Removed auto_now_add=True so the user can select past dates
    category = models.CharField(max_length=100)
    
    # New fields to match your HTML form
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_recurring = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - ${self.amount}"

class Goal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deadline = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class Challenge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    percentage = models.FloatField(default=0.0)
    type = models.CharField(max_length=100, default='savings')
    amount = models.FloatField(default=0.0)
    members = models.IntegerField(default=1)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='challenges', blank=True)

    def __str__(self):
        return self.name