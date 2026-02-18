#!/usr/bin/env python
"""
EraRide API Test Script
Run this to test authentication APIs
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_register():
    print("\n🧪 Testing Registration...")
    data = {
        "email": "student@geu.ac.in",
        "password": "test123456",
        "name": "Test Student",
        "phone": "9876543210",
        "college_id": "GEU2021001",
        "course": "B.Tech Computer Science",
        "year": 3,
        "role": "rider"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register/", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_verify_otp(email, otp):
    print("\n🧪 Testing OTP Verification...")
    data = {
        "email": email,
        "otp": otp
    }
    
    response = requests.post(f"{BASE_URL}/auth/verify-otp/", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_login():
    print("\n🧪 Testing Login...")
    data = {
        "email": "student@geu.ac.in",
        "password": "test123456"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_profile(token):
    print("\n🧪 Testing Get Profile...")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/profile/", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 EraRide API Testing")
    print("=" * 50)
    print("\n⚠️  Make sure Django server is running:")
    print("   python manage.py runserver")
    print("\n" + "=" * 50)
    
    try:
        # Test Registration
        reg_response = test_register()
        
        if 'otp' in reg_response:
            # Test OTP Verification
            verify_response = test_verify_otp(
                reg_response['email'], 
                reg_response['otp']
            )
            
            if 'access_token' in verify_response:
                # Test Profile
                test_profile(verify_response['access_token'])
                
                print("\n" + "=" * 50)
                print("✅ All tests passed!")
                print("=" * 50)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to server")
        print("   Make sure Django server is running:")
        print("   python manage.py runserver")
    except Exception as e:
        print(f"\n❌ Error: {e}")
