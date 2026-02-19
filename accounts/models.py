from django.contrib.auth.models import AbstractUser
from django.db import models
from rides.models import Booking

class User(AbstractUser):
    # SRS 4 & 5.1: Roles
    is_rider = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False) # For custom admin roles
    phone = models.CharField(max_length=15, unique=True)
    profile_pic = models.ImageField(upload_to='profiles/', null=True, blank=True)

class DriverProfile(models.Model):
    # SRS 5.2: Driver Module
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_data')
    license_number = models.CharField(max_length=50, unique=True)
    is_verified = models.BooleanField(default=False) # SRS 5.3: Admin approval
    is_available = models.BooleanField(default=True) # SRS 5.2: Status
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)

    def __str__(self):
        return f"Driver: {self.user.username}"
    
