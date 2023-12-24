from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

from utils.ANN import user_symptoms_utils
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
            return redirect('dashboard')
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


@login_required
def dashboard_view(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    data = {
        'name': first_name + ' ' + last_name,
    }
    return render(request, 'dashboard.html', data)


@login_required
def diagnose_machine_view(request):
    predicted_disease = None  # Initialize predicted_disease

    if request.method == 'POST':
        # Retrieve symptoms from the POST request
        symptom_1 = request.POST.get('symptom_1', '')
        symptom_2 = request.POST.get('symptom_2', '')
        symptom_3 = request.POST.get('symptom_3', '')
        symptom_4 = request.POST.get('symptom_4', '')
        symptom_5 = request.POST.get('symptom_5', '')

        # Perform your diagnosis using these symptoms
        predicted_disease = user_symptoms_utils(symptom_1, symptom_2, symptom_3, symptom_4, symptom_5)

        # Store predicted_disease in session
        request.session['predicted_disease'] = predicted_disease

        data = {
            'predicted_disease': predicted_disease,
        }
        return render(request, 'diagnose.html', data)

    if 'predicted_disease' in request.session:
        predicted_disease = request.session['predicted_disease']

    data = {
        'predicted_disease': predicted_disease,
    }
    return render(request, 'diagnose.html', data)
