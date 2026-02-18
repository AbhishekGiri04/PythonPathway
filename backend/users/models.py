from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('rider', 'Rider'),
        ('driver', 'Driver'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='rider')
    college_id = models.CharField(max_length=50)
    course = models.CharField(max_length=100)
    year = models.IntegerField()
    profile_photo = models.ImageField(upload_to='profiles/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    emergency_contact = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']
    
    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'users'

class DriverProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    vehicle_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=100)
    vehicle_color = models.CharField(max_length=50, blank=True)
    dl_number = models.CharField(max_length=50, unique=True)
    dl_expiry_date = models.DateField()
    dl_photo = models.ImageField(upload_to='documents/dl/')
    rc_photo = models.ImageField(upload_to='documents/rc/')
    insurance_photo = models.ImageField(upload_to='documents/insurance/')
    insurance_expiry_date = models.DateField()
    is_documents_verified = models.BooleanField(default=False)
    total_rides = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.name} - {self.vehicle_number}"
    
    class Meta:
        db_table = 'driver_profiles'

class OTPVerification(models.Model):
    email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'otp_verifications'
