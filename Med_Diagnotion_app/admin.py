from django.contrib import admin
from .models import CustomUser,Diagnosis

# Register your models here.


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'date_joined', 'gender')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')


class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('user', 'predicted_disease', 'diagnosis_date')
    list_filter = ('predicted_disease', 'diagnosis_date')
    search_fields = ('predicted_disease', 'symptom_1', 'symptom_2', 'symptom_3', 'symptom_4', 'symptom_5')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Diagnosis, DiagnosisAdmin)
