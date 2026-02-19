from django.db import models
from django.conf import settings

class Vehicle(models.Model):
    # SRS 5.3: Categories
    CATEGORY_CHOICES = [
        ('bike', 'Bike'),
        ('auto', 'Auto'),
        ('cab', 'Cab'),
    ]
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    plate_number = models.CharField(max_length=20, unique=True)
    model_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.category} - {self.plate_number}"

class Booking(models.Model):
    # SRS 5.4: Trip Status Updates
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('on_trip', 'On Trip'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    rider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    vehicle_type = models.CharField(max_length=10) # Cab/Bike/Auto requested
    pickup_location = models.CharField(max_length=255)
    drop_location = models.CharField(max_length=255)
    estimated_fare = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} - {self.status}"
    
class Payment(models.Model):
    booking = models.OneToOneField(
        'Booking', 
        on_delete=models.CASCADE, 
        related_name='ride_payment' # Changed this to be unique
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, default='Paid')