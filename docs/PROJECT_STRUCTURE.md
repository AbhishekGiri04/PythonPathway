# EraRide - Project Structure

## 📁 Complete Folder Structure

```
EraRide/
│
├── backend/                          # Django Backend
│   ├── eraride/                      # Main project settings
│   │   ├── __init__.py
│   │   ├── settings.py               # Django settings
│   │   ├── urls.py                   # Main URL routing
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   ├── users/                        # User management app
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── models.py                 # User, DriverProfile models
│   │   ├── serializers.py            # DRF serializers
│   │   ├── views.py                  # API views
│   │   ├── urls.py                   # App URLs
│   │   ├── admin.py                  # Admin configuration
│   │   └── validators.py             # Email domain validation
│   │
│   ├── rides/                        # Ride management app
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── models.py                 # Route, Ride models
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── bookings/                     # Booking system app
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── models.py                 # Booking model
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── ratings/                      # Rating system app
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── models.py                 # Rating model
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── complaints/                   # Complaint system app
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── models.py                 # Complaint model
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── face_verification/            # AI face verification
│   │   ├── __init__.py
│   │   ├── face_detector.py          # Face detection logic
│   │   ├── face_matcher.py           # Face matching logic
│   │   ├── utils.py                  # Helper functions
│   │   └── models/                   # Pre-trained models
│   │
│   ├── utils/                        # Shared utilities
│   │   ├── __init__.py
│   │   ├── otp.py                    # OTP generation
│   │   ├── email.py                  # Email sending
│   │   ├── sms.py                    # SMS sending (Twilio)
│   │   └── cloudinary.py             # Image upload
│   │
│   ├── media/                        # Uploaded files (local dev)
│   │   ├── profile_photos/
│   │   ├── documents/
│   │   └── face_images/
│   │
│   ├── static/                       # Static files
│   │
│   ├── manage.py                     # Django management
│   ├── requirements.txt              # Python dependencies
│   ├── .env                          # Environment variables
│   ├── .env.example                  # Env template
│   ├── .gitignore
│   └── README.md
│
├── frontend/                         # Flutter Frontend
│   └── eraride_app/
│       ├── android/                  # Android config
│       ├── ios/                      # iOS config
│       ├── lib/
│       │   ├── main.dart             # App entry point
│       │   │
│       │   ├── models/               # Data models
│       │   │   ├── user.dart
│       │   │   ├── ride.dart
│       │   │   ├── booking.dart
│       │   │   └── route.dart
│       │   │
│       │   ├── services/             # API services
│       │   │   ├── api_service.dart
│       │   │   ├── auth_service.dart
│       │   │   ├── ride_service.dart
│       │   │   └── storage_service.dart
│       │   │
│       │   ├── providers/            # State management
│       │   │   ├── auth_provider.dart
│       │   │   ├── ride_provider.dart
│       │   │   └── booking_provider.dart
│       │   │
│       │   ├── screens/              # UI screens
│       │   │   ├── splash_screen.dart
│       │   │   ├── auth/
│       │   │   │   ├── login_screen.dart
│       │   │   │   ├── register_screen.dart
│       │   │   │   └── otp_screen.dart
│       │   │   ├── home/
│       │   │   │   ├── home_screen.dart
│       │   │   │   └── route_selection_screen.dart
│       │   │   ├── rides/
│       │   │   │   ├── ride_list_screen.dart
│       │   │   │   ├── ride_details_screen.dart
│       │   │   │   └── create_ride_screen.dart
│       │   │   ├── bookings/
│       │   │   │   ├── my_bookings_screen.dart
│       │   │   │   └── booking_confirmation_screen.dart
│       │   │   ├── profile/
│       │   │   │   ├── profile_screen.dart
│       │   │   │   └── driver_profile_screen.dart
│       │   │   └── face/
│       │   │       └── face_verification_screen.dart
│       │   │
│       │   ├── widgets/              # Reusable widgets
│       │   │   ├── custom_button.dart
│       │   │   ├── ride_card.dart
│       │   │   ├── booking_card.dart
│       │   │   └── rating_widget.dart
│       │   │
│       │   ├── utils/                # Utilities
│       │   │   ├── constants.dart
│       │   │   ├── validators.dart
│       │   │   └── helpers.dart
│       │   │
│       │   └── theme/                # App theme
│       │       └── app_theme.dart
│       │
│       ├── assets/                   # Images, fonts
│       │   ├── images/
│       │   └── fonts/
│       │
│       ├── test/                     # Unit tests
│       ├── pubspec.yaml              # Flutter dependencies
│       └── README.md
│
├── docs/                             # Documentation
│   ├── PROJECT_OVERVIEW.md           # Complete project details
│   ├── DEVELOPMENT_GUIDE.md          # Step-by-step guide
│   ├── DATABASE_SCHEMA.md            # Database design
│   ├── API_DOCUMENTATION.md          # API endpoints
│   ├── QUICK_START.md                # Quick setup guide
│   └── DEPLOYMENT.md                 # Deployment guide
│
├── .git/                             # Git repository
├── .gitignore                        # Git ignore rules
├── LICENSE                           # License file
└── README.md                         # Main readme
```

---

## 🎯 Key Directories Explained

### Backend Structure

#### `eraride/` - Main Project
- Django settings and configuration
- URL routing
- WSGI/ASGI configuration

#### `users/` - User Management
- Custom User model
- Driver profile
- Authentication APIs
- Profile management

#### `rides/` - Ride System
- Route model (fixed routes)
- Ride model (ride instances)
- Ride creation/search APIs

#### `bookings/` - Booking System
- Booking model
- Booking creation/cancellation
- Booking history

#### `ratings/` - Rating System
- Rating model
- Rating submission
- Average rating calculation

#### `complaints/` - Complaint System
- Complaint model
- Complaint submission
- Admin review

#### `face_verification/` - AI Module
- Face detection
- Face embedding extraction
- Face matching algorithm

#### `utils/` - Shared Code
- OTP generation
- Email/SMS sending
- Image upload to Cloudinary

---

### Frontend Structure

#### `models/` - Data Models
- Dart classes for API responses
- Data serialization

#### `services/` - API Integration
- HTTP requests
- Token management
- Local storage

#### `providers/` - State Management
- Provider pattern
- App state
- User session

#### `screens/` - UI Pages
- All app screens
- Navigation

#### `widgets/` - Reusable Components
- Custom buttons
- Cards
- Form fields

---

## 📦 Dependencies

### Backend (Python)
```
Django==4.2.7
djangorestframework==3.14.0
psycopg2-binary==2.9.9
djangorestframework-simplejwt==5.3.0
opencv-python==4.8.1.78
deepface==0.0.79
cloudinary==1.36.0
```

### Frontend (Flutter)
```yaml
http: ^1.1.0
provider: ^6.1.1
shared_preferences: ^2.2.2
image_picker: ^1.0.5
camera: ^0.10.5
```

---

## 🔄 Data Flow

```
User (Flutter App)
    ↓
HTTP Request
    ↓
Django REST API
    ↓
Business Logic (Views)
    ↓
Database (PostgreSQL)
    ↓
Response (JSON)
    ↓
Flutter App (UI Update)
```

---

## 🚀 Development Workflow

1. **Backend First**
   - Create models
   - Run migrations
   - Build APIs
   - Test with Postman

2. **Frontend Second**
   - Create UI screens
   - Integrate APIs
   - Test on emulator
   - Build APK

3. **Integration**
   - Connect frontend to backend
   - End-to-end testing
   - Bug fixes

4. **Deployment**
   - Deploy backend to cloud
   - Build production APK
   - Beta testing

---

## 📝 File Naming Conventions

### Backend (Python)
- `snake_case` for files: `user_profile.py`
- `PascalCase` for classes: `UserProfile`
- `snake_case` for functions: `get_user_profile()`

### Frontend (Dart)
- `snake_case` for files: `user_profile.dart`
- `PascalCase` for classes: `UserProfile`
- `camelCase` for variables: `userProfile`

---

## 🎨 Code Organization Tips

### Keep It Simple
- One model per file
- One API endpoint per view
- One screen per file

### Follow DRY (Don't Repeat Yourself)
- Create reusable functions
- Use mixins for common logic
- Share utilities across apps

### Write Clean Code
- Meaningful variable names
- Add docstrings
- Comment complex logic

---

## 🔐 Security Structure

```
Authentication Layer (JWT)
    ↓
Permission Layer (IsAuthenticated)
    ↓
Validation Layer (Serializers)
    ↓
Business Logic (Views)
    ↓
Database Layer (Models)
```

---

## 📊 Current Status

```
✅ Project structure created
✅ Documentation written
⏳ Backend setup pending
⏳ Models creation pending
⏳ API development pending
⏳ Frontend development pending
```

---

## 🎯 Next Action

**Start with:** `docs/QUICK_START.md`

Follow the 30-minute setup guide to get your backend running!
