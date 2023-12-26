from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('signup', views.signup_view, name='signup'),
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('diagnose', views.diagnose_machine_view, name='diagnose'),
    path('profile', views.profile_view, name='profile'),
    path('edit-profile', views.edit_profile, name='edit-profile'),
    path('logout', views.logout_view, name='logout'),
    path('diagnose-history', views.history_view, name='diagnose-history'),
]
