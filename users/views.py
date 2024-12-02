import hmac
from django.contrib import admin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login  # Import Django's login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .forms import RegisterForm
from .models import User

# הסרת הפונקציה verify_password מכיוון שנעשה שימוש ב- authenticate של Django

def user_login(request):
    """Function to handle user login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # השתמש ב-authenticate של Django לאימות המשתמש
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # אם המשתמש מאומת, נכנס לחשבון
            django_login(request, user)  # Use Django's login function to log the user in
            return redirect('home')  # Redirect to a home page or dashboard
        else:
            # אם הסיסמה או שם המשתמש לא נכונים, הצג הודעה
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
