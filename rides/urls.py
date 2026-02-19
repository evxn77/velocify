from django.urls import path
from . import views

urlpatterns = [
    # Ride Initiation (Rider Side)
    path('request/', views.request_ride, name='request_ride'),
    path('searching/<int:ride_id>/', views.ride_searching, name='ride_searching'),
    
    # Trip Management (Driver Side)
    path('active-trips/', views.active_trips, name='active_trips'),
    path('accept/<int:ride_id>/', views.accept_ride, name='accept_ride'),
    path('update-status/<int:ride_id>/', views.update_ride_status, name='update_ride_status'),
    
    # Post-Trip & Billing
    path('status/<int:ride_id>/', views.ride_status, name='ride_status'),
    path('invoice/<int:ride_id>/', views.ride_invoice, name='ride_invoice'),
    path('status/<int:ride_id>/', views.ride_status, name='ride_status'),
]