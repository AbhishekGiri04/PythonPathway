# 🚀 EraRide - Quick Start Guide

## What to Do RIGHT NOW (30 Minutes)

### Step 1: Setup Backend (10 mins)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate  # Windows

# Install Django
pip install django djangorestframework django-cors-headers python-decouple psycopg2-binary

# Create Django project
django-admin startproject eraride .

# Create apps
python manage.py startapp users
python manage.py startapp rides
python manage.py startapp bookings
```

---

### Step 2: Configure Settings (10 mins)

Edit `backend/eraride/settings.py`:

```python
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'corsheaders',
    
    # Local apps
    'users',
    'rides',
    'bookings',
]

# Add CORS middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Add this
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
]

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Custom user model
AUTH_USER_MODEL = 'users.User'
```

---

### Step 3: Create User Model (10 mins)

Edit `backend/users/models.py`:

```python
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
    profile_photo_url = models.URLField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']
    
    def __str__(self):
        return self.email
```

---

### Step 4: Run Migrations

```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

---

### Step 5: Test Server

```bash
# Run server
python manage.py runserver

# Visit: http://localhost:8000/admin
```

---

## ✅ Success Checklist

After 30 minutes, you should have:
- [x] Django project created
- [x] Virtual environment setup
- [x] User model created
- [x] Database migrated
- [x] Admin panel accessible

---

## 🎯 Next Steps (Tomorrow)

1. Create Route model
2. Create Ride model
3. Create Booking model
4. Build registration API
5. Build login API

---

## 📚 Resources

- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- JWT Auth: https://django-rest-framework-simplejwt.readthedocs.io/

---

## 🆘 Common Issues

### Issue: "No module named 'django'"
**Solution:** Activate virtual environment first

### Issue: "psycopg2 installation failed"
**Solution:** `pip install psycopg2-binary` instead

### Issue: "Port 8000 already in use"
**Solution:** `python manage.py runserver 8001`

---

## 💪 You Got This!

Start with these 30 minutes. Don't overthink. Just execute.

**Tomorrow:** We'll build the authentication API.
