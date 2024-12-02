import hmac
import hashlib
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login  # Import Django's login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .forms import RegisterForm
from .models import User

def verify_password(stored_password, entered_password):
    """Verify password by comparing entered password with the stored hash"""
    # Split the stored password into salt and hash
    salt, stored_hash = stored_password.split('$')

    # Re-hash the entered password with the stored salt
    entered_hash = hmac.new(salt.encode(), entered_password.encode(), hashlib.sha256).hexdigest()

    # Compare the hashes
    return stored_hash == entered_hash


def user_login(request):
    """Function to handle user login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Fetch the user from the database
        user = User.objects.get(username=username)

        # Verify the password using the stored hash and salt
        if verify_password(user.password, password):
            # If the password is correct, log the user in
            django_login(request, user)  # Use Django's login function to log the user in
            return redirect('home')  # Redirect to a home page or dashboard
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})

    return render(request, 'users/login.html')


def register(request):
    """Function to handle user registration"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user to the database
            return redirect('login')  # Redirect to the login page
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


def home(request):
    """Function to render the home page"""
    return render(request, 'users/home.html')  # Return a home template


def password_change(request):
    """Function to handle password change"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            # Save the new password
            user = form.save()
            # Update the session to prevent the user from being logged out
            update_session_auth_hash(request, user)
            return redirect('password_change_done')  # Redirect to password change confirmation page
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'users/password_change.html', {'form': form})


def password_change_done(request):
    """Function to display the password change success message"""
    return render(request, 'users/password_change_done.html')
