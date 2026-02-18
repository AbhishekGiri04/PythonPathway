from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta
import random
from .models import User, OTPVerification, DriverProfile
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, 
    UserSerializer, DriverProfileSerializer, OTPVerificationSerializer
)

def generate_otp():
    return str(random.randint(100000, 999999))

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate OTP
        otp_code = generate_otp()
        OTPVerification.objects.create(
            email=user.email,
            otp_code=otp_code,
            expires_at=timezone.now() + timedelta(minutes=5)
        )
        
        # TODO: Send OTP via email
        print(f"OTP for {user.email}: {otp_code}")  # For development
        
        return Response({
            'message': 'Registration successful. OTP sent to email.',
            'email': user.email,
            'otp': otp_code  # Remove in production
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    serializer = OTPVerificationSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        
        try:
            otp_obj = OTPVerification.objects.filter(
                email=email, 
                otp_code=otp,
                is_verified=False,
                expires_at__gt=timezone.now()
            ).latest('created_at')
            
            user = User.objects.get(email=email)
            user.is_verified = True
            user.save()
            
            otp_obj.is_verified = True
            otp_obj.save()
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Account verified successfully',
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
            
        except OTPVerification.DoesNotExist:
            return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        data = serializer.data
        
        # Add driver profile if exists
        if hasattr(request.user, 'driver_profile'):
            data['driver_profile'] = DriverProfileSerializer(request.user.driver_profile).data
        
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_driver_profile(request):
    if request.user.role != 'driver':
        return Response({'error': 'Only drivers can create driver profile'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    if hasattr(request.user, 'driver_profile'):
        return Response({'error': 'Driver profile already exists'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    serializer = DriverProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({
            'message': 'Driver profile created. Documents under verification.',
            'driver_profile': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
