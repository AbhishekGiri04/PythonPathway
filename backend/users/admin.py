from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, DriverProfile, OTPVerification

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'name', 'role', 'is_verified', 'is_active', 'created_at']
    list_filter = ['role', 'is_verified', 'is_active']
    search_fields = ['email', 'name', 'phone', 'college_id']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'phone', 'college_id', 'course', 'year', 'profile_photo', 'emergency_contact')}),
        ('Permissions', {'fields': ('role', 'is_verified', 'is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_login']
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone', 'password1', 'password2', 'role'),
        }),
    )

@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'vehicle_number', 'vehicle_type', 'is_documents_verified', 'average_rating', 'total_rides']
    list_filter = ['is_documents_verified', 'vehicle_type']
    search_fields = ['user__name', 'user__email', 'vehicle_number', 'dl_number']
    readonly_fields = ['total_rides', 'average_rating', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Vehicle Info', {'fields': ('vehicle_number', 'vehicle_type', 'vehicle_model', 'vehicle_color')}),
        ('Documents', {'fields': ('dl_number', 'dl_expiry_date', 'dl_photo', 'rc_photo', 'insurance_photo', 'insurance_expiry_date')}),
        ('Verification', {'fields': ('is_documents_verified',)}),
        ('Statistics', {'fields': ('total_rides', 'average_rating')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ['email', 'otp_code', 'is_verified', 'expires_at', 'created_at']
    list_filter = ['is_verified']
    search_fields = ['email']
    readonly_fields = ['created_at']
