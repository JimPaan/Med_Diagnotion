from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import CustomUser

# Create your views here.


def index(request):
    name = 'Muaz'
    age = 25
    gender = 'male'
    data = {
        'name': name,
        'age': age,
        'gender': gender,
    }
    return render(request, 'index.html', data)


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect('login')

    return render(request, 'login.html')


def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
        gender = request.POST.get('gender')

        print(email, first_name, last_name, password, confirm_password, gender)

        # Check if passwords match
        if password != confirm_password:
            # Handle password mismatch error
            messages.error(request, 'Password do not match!')
            return redirect('signup')

        # Create user
        user = CustomUser.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            gender=gender,
            date_joined=timezone.now()
        )

        return redirect('login')
    return render(request, 'signup.html')


def dashboard_view(request):
    return render(request, 'dashboard.html')
