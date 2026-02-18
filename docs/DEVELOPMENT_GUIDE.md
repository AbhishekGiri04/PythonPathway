# EraRide - Step-by-Step Development Guide

## 🎯 Build Strategy: Start Small, Iterate Fast

---

## Phase 1: Foundation (Week 1-2)

### Step 1: Backend Setup ✅
- [x] Create project structure
- [x] Setup requirements.txt
- [x] Create .env template
- [ ] Initialize Django project
- [ ] Setup PostgreSQL connection

**Commands:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install django djangorestframework
django-admin startproject eraride .
```

---

### Step 2: Database Models (Week 1)

**Priority Order:**
1. User Model (authentication)
2. Profile Model (student details)
3. Route Model (fixed routes)
4. Ride Model (ride creation)
5. Booking Model (ride booking)

**Create apps:**
```bash
python manage.py startapp users
python manage.py startapp rides
python manage.py startapp bookings
```

---

### Step 3: Authentication System (Week 1-2)

**Build in this order:**

#### 3.1 Basic Registration
- Email validation (@geu.ac.in domain check)
- Password creation
- College ID input

#### 3.2 OTP Verification
- Send OTP to email
- Verify OTP
- Activate account

#### 3.3 Login System
- JWT token generation
- Token refresh
- Logout

**API Endpoints:**
```
POST /api/auth/register/
POST /api/auth/verify-otp/
POST /api/auth/login/
POST /api/auth/logout/
POST /api/auth/refresh-token/
```

---

## Phase 2: Core Features (Week 3-4)

### Step 4: Profile System (Week 3)

#### 4.1 Rider Profile
- Name, Course, Year
- Phone number
- Profile photo

#### 4.2 Driver Profile
- All rider fields +
- Vehicle details
- Document upload (DL, RC, Insurance)
- Verification status

**API Endpoints:**
```
GET /api/profile/
PUT /api/profile/
POST /api/profile/driver/documents/
```

---

### Step 5: Fixed Route System (Week 3)

**Initial Routes (Admin creates these):**
1. Rajpur Road → GEU Campus
2. Clock Tower → GEU Campus
3. Patel Nagar → GEU Campus
4. Ballupur → GEHU Campus
5. Mussoorie Diversion → GEHU Campus

**Time Slots:**
- Morning: 8:00 AM, 8:30 AM, 9:00 AM
- Evening: 4:00 PM, 5:00 PM, 6:00 PM

**API Endpoints:**
```
GET /api/routes/              # List all routes
GET /api/routes/{id}/         # Route details
```

---

### Step 6: Ride Creation (Week 4)

**Driver can:**
- Select route
- Select date
- Select time slot
- Set available seats (max 4)
- Set price per seat

**API Endpoints:**
```
POST /api/rides/create/
GET /api/rides/my-rides/      # Driver's rides
PUT /api/rides/{id}/update/
DELETE /api/rides/{id}/cancel/
```

---

### Step 7: Ride Search & Booking (Week 4)

**Rider can:**
- Search rides by route
- Filter by date & time
- View available seats
- Book a seat

**API Endpoints:**
```
GET /api/rides/search/?route={id}&date={date}&time={time}
POST /api/bookings/create/
GET /api/bookings/my-bookings/
PUT /api/bookings/{id}/cancel/
```

---

## Phase 3: Safety Features (Week 5-6)

### Step 8: Basic Safety (Week 5)

#### 8.1 Ride History
- Log all completed rides
- Show past bookings

#### 8.2 Emergency Contact
- Add emergency contact in profile
- Emergency button in active ride

#### 8.3 Complaint System
- Report driver/rider
- Complaint categories
- Admin review

**API Endpoints:**
```
GET /api/rides/history/
POST /api/complaints/create/
GET /api/complaints/my-complaints/
```

---

### Step 9: Rating System (Week 5)

**After ride completion:**
- Rate driver/rider (1-5 stars)
- Optional review comment
- Display average rating on profile

**API Endpoints:**
```
POST /api/ratings/create/
GET /api/ratings/user/{id}/
```

---

### Step 10: Face Verification (Week 6)

**AI Module - Build separately:**

#### 10.1 Face Registration
- Upload ID card photo
- Extract face
- Store face embedding

#### 10.2 Face Verification
- Capture live selfie before ride
- Compare with stored embedding
- Approve/reject

**API Endpoints:**
```
POST /api/face/register/
POST /api/face/verify/
```

**Python Libraries:**
```python
from deepface import DeepFace
import cv2
```

---

## Phase 4: Admin Panel (Week 7)

### Step 11: Admin Dashboard

**Admin can:**
- View all users
- Approve driver documents
- View all rides
- Handle complaints
- Suspend accounts
- View statistics

**Django Admin customization:**
```python
# users/admin.py
from django.contrib import admin
from .models import User, DriverProfile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'role', 'is_verified']
    list_filter = ['role', 'is_verified']
    search_fields = ['email', 'name']
```

---

## Phase 5: Flutter App (Week 8-10)

### Step 12: Flutter Setup (Week 8)

```bash
cd frontend
flutter create eraride_app
cd eraride_app
```

**Dependencies (pubspec.yaml):**
```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0
  provider: ^6.1.1
  shared_preferences: ^2.2.2
  image_picker: ^1.0.5
  geolocator: ^10.1.0
  google_maps_flutter: ^2.5.0
  camera: ^0.10.5
```

---

### Step 13: App Screens (Week 8-9)

**Build order:**
1. Splash Screen
2. Login/Register Screen
3. Home Screen
4. Route Selection Screen
5. Ride List Screen
6. Booking Confirmation Screen
7. Profile Screen
8. My Rides Screen
9. Ride History Screen

---

### Step 14: API Integration (Week 9-10)

**Create API service:**
```dart
// lib/services/api_service.dart
class ApiService {
  static const String baseUrl = 'http://localhost:8000/api';
  
  Future<Map<String, dynamic>> login(String email, String password) async {
    // API call
  }
  
  Future<List<Ride>> searchRides(String routeId, String date) async {
    // API call
  }
}
```

---

## Phase 6: Testing & Launch (Week 11-12)

### Step 15: Testing (Week 11)

**Test scenarios:**
- [ ] User registration & login
- [ ] Driver document upload
- [ ] Ride creation
- [ ] Ride search & booking
- [ ] Booking cancellation
- [ ] Rating system
- [ ] Complaint submission

---

### Step 16: Beta Launch (Week 12)

**Launch checklist:**
- [ ] Deploy backend (Railway/Render)
- [ ] Setup PostgreSQL on cloud
- [ ] Configure domain & HTTPS
- [ ] Build Flutter APK
- [ ] Test on real devices
- [ ] Onboard 5-10 beta users
- [ ] Collect feedback

---

## 📊 Development Tracking

### Current Status: Phase 1 - Foundation
- [x] Project structure created
- [x] Documentation written
- [ ] Django project initialized
- [ ] Database models created
- [ ] Authentication system built

---

## 🎯 Immediate Next Steps

### What to do RIGHT NOW:

1. **Setup Backend (30 mins)**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install django djangorestframework django-cors-headers python-decouple
django-admin startproject eraride .
```

2. **Create User App (15 mins)**
```bash
python manage.py startapp users
```

3. **Define User Model (1 hour)**
- Create custom User model
- Add role field (driver/rider)
- Add college_id field

4. **Test Database Connection (30 mins)**
- Setup PostgreSQL
- Run migrations
- Create superuser

---

## 💡 Pro Tips

### Do's ✅
- Commit code daily
- Test each feature before moving forward
- Keep API documentation updated
- Write simple, readable code

### Don'ts ❌
- Don't build everything at once
- Don't skip testing
- Don't hardcode values
- Don't ignore errors

---

## 🚀 Success Metrics

**Week 1-2:** Authentication working
**Week 3-4:** Can create and book rides
**Week 5-6:** Safety features implemented
**Week 7-8:** Admin panel + Flutter UI
**Week 9-10:** Full app integration
**Week 11-12:** Beta launch ready

---

## 📞 When You're Stuck

1. Check Django/Flutter documentation
2. Search Stack Overflow
3. Review this guide
4. Break problem into smaller steps
5. Ask for help with specific error

---

## 🏆 Final Goal

**By end of 12 weeks:**
- ✅ Working mobile app
- ✅ Backend API deployed
- ✅ 10+ beta users
- ✅ Strong resume project
- ✅ Potential startup

**Let's build this! 🔥**
