from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum, Count
from rides.models import Booking, Payment
from django.contrib.auth import get_user_model

User = get_user_model()

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    stats = {
        'total_revenue': Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0,
        'total_rides': Booking.objects.count(),
        'active_drivers': User.objects.filter(is_driver=True).count(),
        'total_riders': User.objects.filter(is_rider=True).count(),
        'pending_rides': Booking.objects.filter(status='pending').count(),
    }
    
    recent_bookings = Booking.objects.select_related('rider').order_by('-created_at')[:8]
    
    return render(request, 'velocify_admin/dashboard.html', {'stats': stats, 'recent_bookings': recent_bookings})