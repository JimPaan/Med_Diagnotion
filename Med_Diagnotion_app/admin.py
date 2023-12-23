from django.contrib import admin
from .models import CustomUser

# Register your models here.


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'date_joined', 'gender')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')


admin.site.register(CustomUser, CustomUserAdmin)
