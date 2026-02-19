from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

# --- The Registration Form ---
class UserRegisterForm(UserCreationForm):
    ROLE_CHOICES = [
        ('rider', 'Rider (Request Rides)'),
        ('driver', 'Driver (Earn Money)'),
    ]
    
    phone = forms.CharField(
        max_length=15, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'e.g. +91 9876543210'}),
        label="Phone Number"
    )
    
    role = forms.ChoiceField(
        choices=ROLE_CHOICES, 
        widget=forms.RadioSelect, 
        label="Select Your Role"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'phone')

# --- The Login Form (The missing piece) ---
class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'pro-input', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'pro-input', 'placeholder': 'Password'})
    )