from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, DriverProfile
from django.conf import settings

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'phone', 'college_id', 'course', 'year', 'role']
    
    def validate_email(self, value):
        domain = value.split('@')[-1]
        if domain not in settings.ALLOWED_EMAIL_DOMAINS:
            raise serializers.ValidationError(f"Email must be from {', '.join(settings.ALLOWED_EMAIL_DOMAINS)}")
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_verified:
            raise serializers.ValidationError("Account not verified. Please verify OTP.")
        data['user'] = user
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'phone', 'role', 'college_id', 'course', 'year', 
                  'profile_photo', 'is_verified', 'emergency_contact', 'created_at']
        read_only_fields = ['id', 'email', 'is_verified', 'created_at']

class DriverProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverProfile
        fields = ['id', 'vehicle_number', 'vehicle_type', 'vehicle_model', 'vehicle_color',
                  'dl_number', 'dl_expiry_date', 'dl_photo', 'rc_photo', 'insurance_photo',
                  'insurance_expiry_date', 'is_documents_verified', 'total_rides', 'average_rating']
        read_only_fields = ['id', 'is_documents_verified', 'total_rides', 'average_rating']

class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
