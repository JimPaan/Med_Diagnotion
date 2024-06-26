from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from utils.ANN import user_symptoms_utils
from .models import CustomUser, Diagnosis, Thread, Post
from .forms import ProfileEditForm, ThreadForm, PostForm


# Create your views here.


def index(request):
    return render(request, 'index.html')


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
    predicted_disease = None

    if request.method == 'POST':
        # Retrieve symptoms from the POST request
        symptom_1 = request.POST.get('option1')
        symptom_2 = request.POST.get('option2')
        symptom_3 = request.POST.get('option3')
        symptom_4 = request.POST.get('option4')
        symptom_5 = request.POST.get('option5')

        # Perform your diagnosis using these symptoms
        predicted_disease = user_symptoms_utils(symptom_1, symptom_2, symptom_3, symptom_4, symptom_5)

        # Store predicted_disease in session
        request.session['predicted_disease'] = predicted_disease

        Diagnosis.objects.create(
            user=request.user,
            symptom_1=symptom_1,
            symptom_2=symptom_2,
            symptom_3=symptom_3,
            symptom_4=symptom_4,
            symptom_5=symptom_5,
            predicted_disease=predicted_disease
        )

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


@login_required
def profile_view(request):
    return render(request, 'profile.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def history_view(request):
    user_history = Diagnosis.objects.filter(user=request.user)

    data = {
        'user_history': user_history,
    }
    return render(request, 'history.html', data)


@login_required
def forum_view(request):
    threads = Thread.objects.all()

    data = {
        'threads': threads,
    }
    return render(request, 'forum.html', data)


@login_required
def create_thread_view(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            return redirect('forum')
    else:
        form = ThreadForm()

    return render(request, 'thread_form.html', {'form': form})



@login_required
def thread_view(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    comments = Post.objects.filter(thread=thread)
    data = {
        'thread': thread,
        'comments': comments,
    }
    return render(request, 'thread_view.html', data)


@login_required
def create_post_view(request, thread_id):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            thread = get_object_or_404(Thread, id=thread_id)
            comment = form.save(commit=False)
            comment.author = request.user
            comment.thread = thread
            comment.save()
            return redirect('forum')
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form, 'thread_id': thread_id})

