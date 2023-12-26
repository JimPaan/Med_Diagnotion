from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=10)
    country = models.CharField(max_length=50, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    occupation = models.CharField(max_length=50, blank=True, null=True)
    mobile_phone = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


class Diagnosis(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    symptom_1 = models.CharField(max_length=100)
    symptom_2 = models.CharField(max_length=100)
    symptom_3 = models.CharField(max_length=100)
    symptom_4 = models.CharField(max_length=100)
    symptom_5 = models.CharField(max_length=100)
    predicted_disease = models.CharField(max_length=100)
    diagnosis_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user}: {self.predicted_disease}'
