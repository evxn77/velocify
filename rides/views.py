from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
import random

# 1. RIDER: Request a new ride
@login_required
def request_ride(request):
    if request.method == "POST":
        pickup = request.POST.get('pickup')
        drop = request.POST.get('drop')
        
        # Simulated Fare Estimation Logic (SRS 5.1)
        distance = random.uniform(2.5, 15.0) 
        base_fare = 50
        fare = round(base_fare + (distance * 12), 2)
        
        ride = Booking.objects.create(
            rider=request.user,
            pickup_location=pickup,
            drop_location=drop,
            estimated_fare=fare,
            status='pending'
        )
        return redirect('ride_searching', ride_id=ride.id)
    
    return render(request, 'rides/request_ride.html')

# 2. RIDER: Searching Animation Screen
@login_required
def ride_searching(request, ride_id):
    ride = get_object_or_404(Booking, id=ride_id)
    # If a driver has already accepted, move to status
    if ride.status != 'pending':
        return redirect('ride_status', ride_id=ride.id)
    return render(request, 'rides/searching.html', {'ride': ride})

# 3. DRIVER: View all pending requests
@login_required
def active_trips(request):
    # Security: Ensure Admin has approved this driver
    if not request.user.is_driver or not request.user.is_active:
        messages.error(request, "Access Denied: Your driver account is not yet authorized by an admin.")
        return redirect('dashboard')
    
    pending_rides = Booking.objects.filter(status='pending').order_by('-created_at')
    return render(request, 'rides/active_trips.html', {'rides': pending_rides})

# 4. DRIVER: Accept a specific ride
@login_required
def accept_ride(request, ride_id):
    ride = get_object_or_404(Booking, id=ride_id)
    
    # Check if already taken
    if ride.driver:
        messages.error(request, "This ride has already been accepted by another driver.")
        return redirect('active_trips')

    ride.driver = request.user 
    ride.status = 'accepted'
    ride.save()
    
    messages.success(request, "Ride accepted. Please proceed to pickup.")
    return redirect('ride_status', ride_id=ride.id)

# 5. GLOBAL: Live Status of the Ride (Consolidated)
@login_required
def ride_status(request, ride_id):
    ride = get_object_or_404(Booking, id=ride_id)
    return render(request, 'rides/status.html', {'ride': ride})

# 6. DRIVER: Unified Status Updater (Pickup -> Reach -> Complete)
@login_required
def update_ride_status(request, ride_id):
    ride = get_object_or_404(Booking, id=ride_id)
    
    # Security Gate
    if request.user != ride.driver:
        messages.error(request, "Unauthorized action.")
        return redirect('dashboard')

    if ride.status == 'accepted':
        ride.status = 'picked_up'
        messages.success(request, "Status: Rider Picked Up.")
        
    elif ride.status == 'picked_up':
        ride.status = 'reached_destination'
        messages.success(request, "Destination Reached. Please enter final fare.")

    elif ride.status == 'reached_destination':
        fare = request.POST.get('final_fare')
        if fare:
            ride.amount = fare 
            ride.status = 'completed'
            ride.save()
            messages.success(request, f"Trip Completed. Final Fare: ₹{fare}")
            return redirect('ride_invoice', ride_id=ride.id) # Go straight to invoice
        else:
            messages.error(request, "Please enter the final fare to complete the ride.")
    
    ride.save()
    return redirect('ride_status', ride_id=ride.id)

# 7. GLOBAL: Final Invoice/Receipt
@login_required
def ride_invoice(request, ride_id):
    ride = get_object_or_404(Booking, id=ride_id)
    # Ensure only the participants (or admin) can see the invoice
    if request.user != ride.rider and request.user != ride.driver and not request.user.is_staff:
        return redirect('dashboard')
        
    return render(request, 'rides/invoice.html', {'ride': ride})