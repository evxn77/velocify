from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import User
from rides.models import Booking
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm

# --- Email Imports ---
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')
           
            subject = 'Welcome to Velocify Titanium'
            context = {
                'username': user.username,
                'role': role.capitalize(),
            }
            html_message = render_to_string('emails/registration_confirm.html', context)
            plain_message = strip_tags(html_message)

            if role == 'driver':
                user.is_driver = True
                user.is_active = False  
                user.save()
                
                
                try:
                    send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [user.email], html_message=html_message)
                except Exception as e: print(f"Mail failure: {e}")

                messages.info(request, "Driver registration submitted. Access is pending Admin approval.")
                return redirect('login')
            else:
                user.is_rider = True
                user.is_active = True   
                user.save()
                
              
                try:
                    send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [user.email], html_message=html_message)
                except Exception as e: print(f"Mail failure: {e}")

                messages.success(request, "Rider account created successfully!")
                login(request, user)
                return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    
                    try:
                        send_mail(
                            'Velocify Security: New Login Detected',
                            f'Hi {user.username}, a new login was recorded for your Velocify account.',
                            settings.EMAIL_HOST_USER,
                            [user.email],
                            fail_silently=True
                        )
                    except: pass

                    return redirect('dashboard')
                else:
                    messages.error(request, "Your account is pending approval by the Administrator.")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def approve_driver(request, user_id):
    if not request.user.is_staff:
        messages.error(request, "Unauthorized: Staff credentials required.")
        return redirect('dashboard')
    
    driver = get_object_or_404(User, id=user_id)
    driver.is_active = True  
    driver.is_driver = True  
    driver.save()
    
    
    try:
        send_mail(
            'Account Activated: Velocify Fleet Console',
            f'Congratulations {driver.username}! Your driver credentials have been verified. You can now log in and accept rides.',
            settings.EMAIL_HOST_USER,
            [driver.email],
            fail_silently=False
        )
    except Exception as e: print(f"Approval mail failed: {e}")
    
    messages.success(request, f"Access Granted: {driver.username} is now an authorized driver.")
    return redirect('dashboard')

@login_required
def dashboard(request):
    context = {}
    user = request.user

    if user.is_staff:
        context['role'] = 'Administrator'
        context['total_rides'] = Booking.objects.count()
        context['active_drivers'] = User.objects.filter(is_driver=True, is_active=True).count()
        context['pending_drivers'] = User.objects.filter(is_driver=True, is_active=False)
        context['recent_ride'] = Booking.objects.filter(rider=user).order_by('-created_at').first()
        context['active_trip'] = Booking.objects.filter(driver=user).exclude(status='completed').first()
    elif user.is_driver:
        if user.is_active:
            context['role'] = 'Driver'
            context['active_trip'] = Booking.objects.filter(driver=user).exclude(status='completed').first()
        else:
            context['role'] = 'Pending Verification'
    else:
        context['role'] = 'Rider'
        context['recent_ride'] = Booking.objects.filter(rider=user).order_by('-created_at').first()

    return render(request, 'accounts/dashboard.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')