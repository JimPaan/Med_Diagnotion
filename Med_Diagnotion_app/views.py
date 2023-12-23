from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

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
