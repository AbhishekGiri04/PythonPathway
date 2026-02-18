from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('auth/register/', views.register, name='register'),
    path('auth/verify-otp/', views.verify_otp, name='verify-otp'),
    path('auth/login/', views.login, name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('profile/', views.profile, name='profile'),
    path('profile/driver/', views.create_driver_profile, name='create-driver-profile'),
]
