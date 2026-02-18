# EraRide - API Documentation

**Base URL:** `http://localhost:8000/api`

**Authentication:** JWT Bearer Token (except auth endpoints)

---

## 📋 Table of Contents
1. [Authentication](#authentication)
2. [User Profile](#user-profile)
3. [Routes](#routes)
4. [Rides](#rides)
5. [Bookings](#bookings)
6. [Ratings](#ratings)
7. [Complaints](#complaints)
8. [Face Verification](#face-verification)

---

## 🔐 Authentication

### 1. Register User
**POST** `/auth/register/`

**Request:**
```json
{
  "email": "student@geu.ac.in",
  "password": "SecurePass123",
  "name": "Abhishek Giri",
  "phone": "+919876543210",
  "college_id": "GEU2021001",
  "course": "B.Tech Computer Science",
  "year": 3,
  "role": "rider"
}
```

**Response:** `201 Created`
```json
{
  "message": "OTP sent to email",
  "email": "student@geu.ac.in",
  "otp_expires_in": 300
}
```

**Validations:**
- Email must end with @geu.ac.in or @gehu.ac.in
- Password min 8 characters
- Phone must be valid Indian number
- Year must be 1-4
- Role must be 'rider' or 'driver'

---

### 2. Verify OTP
**POST** `/auth/verify-otp/`

**Request:**
```json
{
  "email": "student@geu.ac.in",
  "otp": "123456"
}
```

**Response:** `200 OK`
```json
{
  "message": "Account verified successfully",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "uuid",
    "email": "student@geu.ac.in",
    "name": "Abhishek Giri",
    "role": "rider",
    "is_verified": true
  }
}
```

---

### 3. Login
**POST** `/auth/login/`

**Request:**
```json
{
  "email": "student@geu.ac.in",
  "password": "SecurePass123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "uuid",
    "email": "student@geu.ac.in",
    "name": "Abhishek Giri",
    "role": "rider",
    "profile_photo_url": "https://..."
  }
}
```

---

### 4. Refresh Token
**POST** `/auth/refresh/`

**Request:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### 5. Logout
**POST** `/auth/logout/`

**Headers:** `Authorization: Bearer {access_token}`

**Response:** `200 OK`
```json
{
  "message": "Logged out successfully"
}
```

---

## 👤 User Profile

### 6. Get Profile
**GET** `/profile/`

**Headers:** `Authorization: Bearer {access_token}`

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "email": "student@geu.ac.in",
  "name": "Abhishek Giri",
  "phone": "+919876543210",
  "role": "driver",
  "college_id": "GEU2021001",
  "course": "B.Tech Computer Science",
  "year": 3,
  "profile_photo_url": "https://...",
  "emergency_contact": "+919876543211",
  "is_verified": true,
  "created_at": "2024-01-01T10:00:00Z",
  "driver_profile": {
    "vehicle_number": "UK07AB1234",
    "vehicle_type": "Car",
    "vehicle_model": "Maruti Swift",
    "vehicle_color": "White",
    "is_documents_verified": true,
    "total_rides": 25,
    "average_rating": 4.5
  }
}
```

---

### 7. Update Profile
**PUT** `/profile/`

**Headers:** `Authorization: Bearer {access_token}`

**Request:**
```json
{
  "name": "Abhishek Kumar Giri",
  "phone": "+919876543210",
  "emergency_contact": "+919876543211",
  "profile_photo": "base64_encoded_image"
}
```

**Response:** `200 OK`
```json
{
  "message": "Profile updated successfully",
  "profile_photo_url": "https://..."
}
```

---

### 8. Create Driver Profile
**POST** `/profile/driver/`

**Headers:** `Authorization: Bearer {access_token}`

**Request:** (multipart/form-data)
```
vehicle_number: UK07AB1234
vehicle_type: Car
vehicle_model: Maruti Swift
vehicle_color: White
dl_number: DL1234567890
dl_expiry_date: 2028-12-31
dl_photo: [file]
rc_photo: [file]
insurance_photo: [file]
insurance_expiry_date: 2025-12-31
```

**Response:** `201 Created`
```json
{
  "message": "Driver profile created. Documents under verification.",
  "driver_profile": {
    "vehicle_number": "UK07AB1234",
    "is_documents_verified": false
  }
}
```

---

## 🛣️ Routes

### 9. List All Routes
**GET** `/routes/`

**Response:** `200 OK`
```json
{
  "count": 5,
  "routes": [
    {
      "id": "uuid",
      "route_name": "Rajpur Road to GEU",
      "start_location": "Rajpur Road, Dehradun",
      "end_location": "GEU Campus, Dehradun",
      "distance_km": 8.5,
      "estimated_duration_mins": 25,
      "is_active": true
    }
  ]
}
```

---

### 10. Get Route Details
**GET** `/routes/{id}/`

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "route_name": "Rajpur Road to GEU",
  "start_location": "Rajpur Road, Dehradun",
  "start_latitude": 30.3165,
  "start_longitude": 78.0322,
  "end_location": "GEU Campus, Dehradun",
  "end_latitude": 30.2729,
  "end_longitude": 78.0479,
  "distance_km": 8.5,
  "estimated_duration_mins": 25
}
```

---

## 🚗 Rides

### 11. Create Ride (Driver Only)
**POST** `/rides/`

**Headers:** `Authorization: Bearer {access_token}`

**Request:**
```json
{
  "route_id": "uuid",
  "ride_date": "2024-01-15",
  "time_slot": "08:30:00",
  "total_seats": 3,
  "price_per_seat": 50
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "route": {
    "id": "uuid",
    "route_name": "Rajpur Road to GEU"
  },
  "ride_date": "2024-01-15",
  "time_slot": "08:30:00",
  "total_seats": 3,
  "available_seats": 3,
  "price_per_seat": 50,
  "status": "scheduled"
}
```

**Validations:**
- Driver documents must be verified
- Cannot create ride in the past
- Price must be ₹10-₹100
- Total seats max 4

---

### 12. Search Rides
**GET** `/rides/search/`

**Query Parameters:**
- `route_id` (required)
- `date` (required, format: YYYY-MM-DD)
- `time_slot` (optional, format: HH:MM:SS)

**Example:** `/rides/search/?route_id=uuid&date=2024-01-15&time_slot=08:30:00`

**Response:** `200 OK`
```json
{
  "count": 3,
  "rides": [
    {
      "id": "uuid",
      "driver": {
        "id": "uuid",
        "name": "Rahul Sharma",
        "profile_photo_url": "https://...",
        "average_rating": 4.5,
        "total_rides": 25
      },
      "route": {
        "route_name": "Rajpur Road to GEU",
        "distance_km": 8.5
      },
      "ride_date": "2024-01-15",
      "time_slot": "08:30:00",
      "available_seats": 2,
      "price_per_seat": 50,
      "status": "scheduled"
    }
  ]
}
```

---

### 13. Get My Rides (Driver)
**GET** `/rides/my-rides/`

**Headers:** `Authorization: Bearer {access_token}`

**Query Parameters:**
- `status` (optional: scheduled, ongoing, completed, cancelled)

**Response:** `200 OK`
```json
{
  "count": 10,
  "rides": [
    {
      "id": "uuid",
      "route": {
        "route_name": "Rajpur Road to GEU"
      },
      "ride_date": "2024-01-15",
      "time_slot": "08:30:00",
      "total_seats": 3,
      "available_seats": 1,
      "bookings_count": 2,
      "status": "scheduled"
    }
  ]
}
```

---

### 14. Get Ride Details
**GET** `/rides/{id}/`

**Headers:** `Authorization: Bearer {access_token}`

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "driver": {
    "name": "Rahul Sharma",
    "phone": "+919876543210",
    "vehicle_number": "UK07AB1234",
    "vehicle_model": "Maruti Swift"
  },
  "route": {
    "route_name": "Rajpur Road to GEU",
    "start_location": "Rajpur Road",
    "end_location": "GEU Campus"
  },
  "ride_date": "2024-01-15",
  "time_slot": "08:30:00",
  "available_seats": 1,
  "price_per_seat": 50,
  "status": "scheduled",
  "bookings": [
    {
      "rider_name": "Priya Singh",
      "seats_booked": 1,
      "booking_status": "confirmed"
    }
  ]
}
```

---

### 15. Update Ride
**PUT** `/rides/{id}/`

**Headers:** `Authorization: Bearer {access_token}`

**Request:**
```json
{
  "time_slot": "09:00:00",
  "price_per_seat": 60
}
```

**Response:** `200 OK`

**Note:** Can only update if no confirmed bookings

---

### 16. Cancel Ride
**DELETE** `/rides/{id}/`

**Headers:** `Authorization: Bearer {access_token}`

**Request:**
```json
{
  "cancellation_reason": "Vehicle breakdown"
}
```

**Response:** `200 OK`
```json
{
  "message": "Ride cancelled successfully"
}
```

---

## 📅 Bookings

### 17. Create Booking
**POST** `/bookings/`

**Headers:** `Authorization: Bearer {access_token}`

**Request:**
```json
{
  "ride_id": "uuid",
  "seats_booked": 1
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "ride": {
    "driver_name": "Rahul Sharma",
    "route_name": "Rajpur Road to GEU",
    "ride_date": "2024-01-15",
    "time_slot": "08:30:00"
  },
  "seats_booked": 1,
  "total_amount": 50,
  "platform_fee": 10,
  "booking_status": "confirmed",
  "payment_status": "pending"
}
```

**Validations:**
- Cannot book own ride
- Seats must be available
- Cannot book same ride twice

---

### 18. Get My Bookings
**GET** `/bookings/my-bookings/`

**Headers:** `Authorization: Bearer {access_token}`

**Query Parameters:**
- `status` (optional: pending, confirmed, cancelled, completed)

**Response:** `200 OK`
```json
{
  "count": 5,
  "bookings": [
    {
      "id": "uuid",
      "ride": {
        "driver": {
          "name": "Rahul Sharma",
          "phone": "+919876543210",
          "vehicle_number": "UK07AB1234"
        },
        "route_name": "Rajpur Road to GEU",
        "ride_date": "2024-01-15",
        "time_slot": "08:30:00"
      },
      "seats_booked": 1,
      "total_amount": 50,
      "booking_status": "confirmed",
      "booked_at": "2024-01-10T10:00:00Z"
    }
  ]
}
```

---

### 19. Cancel Booking
**PUT** `/bookings/{id}/cancel/`

**Headers:** `Authorization: Bearer {access_token}`

**Request:**
```json
{
  "cancellation_reason": "Change of plans"
}
```

**Response:** `200 OK`
```json
{
  "message": "Booking cancelled successfully",
  "refund_status": "pending"
}
```

---

## ⭐ Ratings

### 20. Create Rating
**POST** `/ratings/`

**Headers:** `Authorization: Bearer {access_token}`

**Request:**
```json
{
  "ride_id": "uuid",
  "rated_to": "uuid",
  "rating": 5,
  "review_text": "Great ride! Very punctual and safe driving."
}
```

**Response:** `201 Created`
```json
{
  "message": "Rating submitted successfully"
}
```

**Validations:**
- Can only rate after ride completion
- Rating must be 1-5
- Can rate only once per ride

---

### 21. Get User Ratings
**GET** `/ratings/user/{user_id}/`

**Response:** `200 OK`
```json
{
  "user": {
    "name": "Rahul Sharma",
    "role": "driver"
  },
  "average_rating": 4.5,
  "total_ratings": 25,
  "ratings": [
    {
      "rating": 5,
      "review_text": "Great ride!",
      "rated_by": "Priya Singh",
      "created_at": "2024-01-10T10:00:00Z"
    }
  ]
}
```

---

## 🚨 Complaints

### 22. Create Complaint
**POST** `/complaints/`

**Headers:** `Authorization: Bearer {access_token}`

**Request:**
```json
{
  "accused_id": "uuid",
  "ride_id": "uuid",
  "complaint_type": "safety",
  "description": "Driver was driving rashly"
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "message": "Complaint submitted successfully. Admin will review.",
  "status": "pending"
}
```

**Complaint Types:**
- safety
- behavior
- payment
- cancellation
- other

---

### 23. Get My Complaints
**GET** `/complaints/my-complaints/`

**Headers:** `Authorization: Bearer {access_token}`

**Response:** `200 OK`
```json
{
  "count": 2,
  "complaints": [
    {
      "id": "uuid",
      "accused": "Rahul Sharma",
      "ride_date": "2024-01-15",
      "complaint_type": "safety",
      "status": "under_review",
      "created_at": "2024-01-15T18:00:00Z"
    }
  ]
}
```

---

## 🤖 Face Verification

### 24. Register Face
**POST** `/face/register/`

**Headers:** `Authorization: Bearer {access_token}`

**Request:** (multipart/form-data)
```
face_image: [file]
```

**Response:** `200 OK`
```json
{
  "message": "Face registered successfully",
  "face_verified": true
}
```

---

### 25. Verify Face
**POST** `/face/verify/`

**Headers:** `Authorization: Bearer {access_token}`

**Request:** (multipart/form-data)
```
face_image: [file]
booking_id: uuid
```

**Response:** `200 OK`
```json
{
  "verified": true,
  "confidence": 0.95,
  "message": "Face verified successfully"
}
```

---

## 📊 Error Responses

### 400 Bad Request
```json
{
  "error": "Validation error",
  "details": {
    "email": ["Invalid email domain"]
  }
}
```

### 401 Unauthorized
```json
{
  "error": "Authentication required",
  "message": "Invalid or expired token"
}
```

### 403 Forbidden
```json
{
  "error": "Permission denied",
  "message": "Driver documents not verified"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found",
  "message": "Ride not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Server error",
  "message": "Something went wrong"
}
```

---

## 🔒 Authentication Header

All protected endpoints require:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 📝 Rate Limiting

- 100 requests per minute per user
- 10 OTP requests per hour per email

---

## 🧪 Testing

**Postman Collection:** Coming soon
**Swagger UI:** http://localhost:8000/api/docs/
