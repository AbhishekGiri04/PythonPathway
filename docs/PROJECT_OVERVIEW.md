# EraRide - Complete Project Documentation

## 1️⃣ Project Overview
**EraRide** is a secure, student-only carpool platform for:
- Graphic Era University (GEU)
- Graphic Era Hill University (GEHU)

**Purpose**: Safe, affordable, verified daily commute for students
**Model**: Cost-sharing campus carpool (NOT commercial taxi)

---

## 2️⃣ Problem Statement
**Students face:**
- High daily commute cost
- Safety concerns
- Unreliable auto/cab services
- No verified campus-only ride option

**EraRide solves:**
✔ Safety via verification
✔ Low-cost commute
✔ Trusted student network
✔ Fixed predictable routes

---

## 3️⃣ Core Features (MVP)

### 🔐 Authentication
- College ID login
- Email domain restriction (@geu.ac.in)
- OTP verification
- Face verification (AI-based)

### 👤 Profile System
**Driver Profile:**
- Name, Course, Year
- Vehicle details
- DL upload
- RC upload
- Insurance upload

**Rider Profile:**
- Name, Course, Year

### 🚗 Ride System
- Fixed routes (Area → Campus)
- Fixed time slots
- Seat availability
- Pre-booking
- Booking confirmation

### 🛡 Safety Features
- Face match before ride
- Verified badge
- Complaint system
- Emergency contact button
- Ride history log

### ⭐ Rating System
- Driver rating
- Rider rating
- Review comments

---

## 4️⃣ Legal Safe Structure

**EraRide acts as:** "Student Ride Matching Platform"
**NOT:** "Commercial Taxi Service"

**Key Points:**
- Cost-sharing model
- Small platform fee only
- Mandatory valid documents
- Terms & conditions page
- Liability disclaimer

---

## 5️⃣ Supply-Demand Strategy

**Phase 1:**
- Only 3–5 fixed major routes
- Morning & Evening slots
- Pre-book only

**Phase 2:**
- Add more areas based on demand data

**Phase 3:**
- Smart AI ride matching

---

## 6️⃣ Tech Stack

### 📱 Frontend
**Flutter (Dart)**
- Single codebase
- Android + iOS
- Fast MVP development

### 🖥 Backend
**Django / FastAPI (Python)**
- Easy AI integration
- Strong backend logic
- REST API

### 🗄 Database
**PostgreSQL**

### ☁ Hosting
- Firebase (Authentication)
- AWS / Render / Railway (Backend)
- Cloudinary (Image storage)

---

## 7️⃣ Face Verification (AI Module)

**Libraries:**
- OpenCV
- FaceNet
- DeepFace (Python)

**Flow:**
1. Upload ID photo
2. Capture live selfie
3. Compare embeddings
4. Approve or reject

---

## 8️⃣ System Architecture

```
User App (Flutter)
    ↓
API (Django REST)
    ↓
Database (PostgreSQL)
    ↓
AI Face Module
    ↓
Cloud Storage
```

---

## 9️⃣ Database Schema

### Users Table
- id (PK)
- name
- email
- phone
- role (driver/rider)
- college_id
- course
- year
- face_embedding
- is_verified
- created_at

### Vehicles Table
- id (PK)
- user_id (FK)
- vehicle_number
- vehicle_type
- vehicle_model
- dl_number
- dl_url
- rc_url
- insurance_url
- is_verified

### Routes Table
- id (PK)
- route_name
- start_location
- end_location
- distance_km
- is_active

### Rides Table
- id (PK)
- driver_id (FK)
- route_id (FK)
- ride_date
- time_slot
- seats_available
- price_per_seat
- status (scheduled/ongoing/completed/cancelled)
- created_at

### Bookings Table
- id (PK)
- ride_id (FK)
- rider_id (FK)
- booking_status (pending/confirmed/cancelled/completed)
- payment_status
- booked_at

### Ratings Table
- id (PK)
- ride_id (FK)
- rated_by (FK)
- rated_to (FK)
- rating (1-5)
- review_text
- created_at

### Complaints Table
- id (PK)
- user_id (FK)
- ride_id (FK)
- complaint_type
- description
- status (pending/resolved)
- created_at

---

## 🔟 App Screens Required

1. Splash Screen
2. Login / Register
3. Face Verification Screen
4. Home Screen
5. Route Selection
6. Ride Listing
7. Booking Confirmation
8. Driver Dashboard
9. Profile Page
10. Complaint Page
11. Ride History

---

## 1️⃣1️⃣ Revenue Model

**Option 1:** ₹5–₹10 per ride platform fee
**Option 2:** Monthly subscription (₹199 unlimited)
**Option 3:** College tie-up funding

---

## 1️⃣2️⃣ Future Expansion

- Multiple colleges
- Corporate carpool
- AI dynamic pricing
- Ride heatmap
- In-app wallet
- Insurance partnership

---

## 1️⃣3️⃣ Security Checklist

✔ JWT authentication
✔ HTTPS only
✔ Role-based access
✔ Document verification
✔ Ride logging
✔ Admin dashboard

---

## 1️⃣4️⃣ Admin Panel Features

Admin can:
- Approve drivers
- Verify documents
- View complaints
- Suspend accounts
- Monitor ride statistics

---

## 1️⃣5️⃣ MVP Development Roadmap

**Month 1:**
- UI Design
- Authentication system
- Basic ride creation

**Month 2:**
- Booking system
- Database integration
- Admin panel

**Month 3:**
- Face verification
- Testing
- Beta launch in one campus

---

## 1️⃣6️⃣ Resume Impact Line

> "Developed EraRide, a secure campus-exclusive carpooling platform integrating AI-based face verification, document validation, and real-time ride matching using Flutter and Django."

---

## 1️⃣7️⃣ Realistic Challenges

- User trust building
- Legal clarity
- Initial driver onboarding
- College permission
- Server cost

---

## 1️⃣8️⃣ Build Difficulty

**Technical Level:** Intermediate to Advanced
**Time Required:** 2–4 months
**Learning Outcome:**
- System Design
- AI Integration
- Full Stack Development
- Startup Thinking

---

## 🏆 Final Evaluation

**Resume Impact:** 9.5/10
**Startup Potential:** 8.5/10
**Learning Value:** 10/10
**Complexity:** High
**Uniqueness:** Strong

---

## 🔥 Development Strategy

**Start Small:**
1. Login system
2. Fixed route ride creation
3. Booking system
4. Then improve iteratively
