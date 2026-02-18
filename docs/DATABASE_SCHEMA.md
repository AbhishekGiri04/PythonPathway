# EraRide - Database Schema

## Overview
PostgreSQL database with 8 main tables

---

## 1. Users Table

**Purpose:** Store all user accounts (both riders and drivers)

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) UNIQUE NOT NULL,
    role VARCHAR(10) NOT NULL CHECK (role IN ('rider', 'driver')),
    college_id VARCHAR(50) NOT NULL,
    course VARCHAR(100) NOT NULL,
    year INTEGER NOT NULL CHECK (year BETWEEN 1 AND 4),
    profile_photo_url TEXT,
    face_embedding BYTEA,
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    emergency_contact VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**
```sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_is_verified ON users(is_verified);
```

---

## 2. Driver_Profiles Table

**Purpose:** Additional information for drivers only

```sql
CREATE TABLE driver_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    vehicle_number VARCHAR(20) UNIQUE NOT NULL,
    vehicle_type VARCHAR(50) NOT NULL,
    vehicle_model VARCHAR(100) NOT NULL,
    vehicle_color VARCHAR(50),
    dl_number VARCHAR(50) UNIQUE NOT NULL,
    dl_expiry_date DATE NOT NULL,
    dl_photo_url TEXT NOT NULL,
    rc_photo_url TEXT NOT NULL,
    insurance_photo_url TEXT NOT NULL,
    insurance_expiry_date DATE NOT NULL,
    is_documents_verified BOOLEAN DEFAULT FALSE,
    verified_by UUID REFERENCES users(id),
    verified_at TIMESTAMP,
    total_rides INTEGER DEFAULT 0,
    average_rating DECIMAL(3,2) DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**
```sql
CREATE INDEX idx_driver_user_id ON driver_profiles(user_id);
CREATE INDEX idx_driver_verified ON driver_profiles(is_documents_verified);
```

---

## 3. Routes Table

**Purpose:** Fixed predefined routes (Admin managed)

```sql
CREATE TABLE routes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    route_name VARCHAR(100) NOT NULL,
    start_location VARCHAR(200) NOT NULL,
    start_latitude DECIMAL(10,8) NOT NULL,
    start_longitude DECIMAL(11,8) NOT NULL,
    end_location VARCHAR(200) NOT NULL,
    end_latitude DECIMAL(10,8) NOT NULL,
    end_longitude DECIMAL(11,8) NOT NULL,
    distance_km DECIMAL(5,2) NOT NULL,
    estimated_duration_mins INTEGER NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Sample Data:**
```sql
INSERT INTO routes (route_name, start_location, end_location, distance_km, estimated_duration_mins) VALUES
('Rajpur Road to GEU', 'Rajpur Road, Dehradun', 'GEU Campus, Dehradun', 8.5, 25),
('Clock Tower to GEU', 'Clock Tower, Dehradun', 'GEU Campus, Dehradun', 6.2, 20),
('Patel Nagar to GEU', 'Patel Nagar, Dehradun', 'GEU Campus, Dehradun', 5.8, 18);
```

---

## 4. Rides Table

**Purpose:** Individual ride instances created by drivers

```sql
CREATE TABLE rides (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    driver_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    route_id UUID NOT NULL REFERENCES routes(id),
    ride_date DATE NOT NULL,
    time_slot TIME NOT NULL,
    total_seats INTEGER NOT NULL CHECK (total_seats BETWEEN 1 AND 4),
    available_seats INTEGER NOT NULL,
    price_per_seat DECIMAL(6,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'ongoing', 'completed', 'cancelled')),
    cancellation_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_available_seats CHECK (available_seats <= total_seats)
);
```

**Indexes:**
```sql
CREATE INDEX idx_rides_driver ON rides(driver_id);
CREATE INDEX idx_rides_route ON rides(route_id);
CREATE INDEX idx_rides_date ON rides(ride_date);
CREATE INDEX idx_rides_status ON rides(status);
CREATE INDEX idx_rides_search ON rides(route_id, ride_date, time_slot, status);
```

---

## 5. Bookings Table

**Purpose:** Track ride bookings by riders

```sql
CREATE TABLE bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ride_id UUID NOT NULL REFERENCES rides(id) ON DELETE CASCADE,
    rider_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    seats_booked INTEGER DEFAULT 1 CHECK (seats_booked >= 1),
    total_amount DECIMAL(6,2) NOT NULL,
    platform_fee DECIMAL(6,2) NOT NULL,
    booking_status VARCHAR(20) DEFAULT 'pending' CHECK (booking_status IN ('pending', 'confirmed', 'cancelled', 'completed')),
    payment_status VARCHAR(20) DEFAULT 'pending' CHECK (payment_status IN ('pending', 'paid', 'refunded')),
    cancellation_reason TEXT,
    face_verified BOOLEAN DEFAULT FALSE,
    face_verified_at TIMESTAMP,
    booked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ride_id, rider_id)
);
```

**Indexes:**
```sql
CREATE INDEX idx_bookings_ride ON bookings(ride_id);
CREATE INDEX idx_bookings_rider ON bookings(rider_id);
CREATE INDEX idx_bookings_status ON bookings(booking_status);
```

---

## 6. Ratings Table

**Purpose:** Store ratings and reviews

```sql
CREATE TABLE ratings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ride_id UUID NOT NULL REFERENCES rides(id) ON DELETE CASCADE,
    rated_by UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    rated_to UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ride_id, rated_by, rated_to)
);
```

**Indexes:**
```sql
CREATE INDEX idx_ratings_rated_to ON ratings(rated_to);
CREATE INDEX idx_ratings_ride ON ratings(ride_id);
```

---

## 7. Complaints Table

**Purpose:** Handle user complaints

```sql
CREATE TABLE complaints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    complainant_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    accused_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    ride_id UUID REFERENCES rides(id) ON DELETE SET NULL,
    complaint_type VARCHAR(50) NOT NULL CHECK (complaint_type IN ('safety', 'behavior', 'payment', 'cancellation', 'other')),
    description TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'under_review', 'resolved', 'rejected')),
    admin_notes TEXT,
    resolved_by UUID REFERENCES users(id),
    resolved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**
```sql
CREATE INDEX idx_complaints_status ON complaints(status);
CREATE INDEX idx_complaints_accused ON complaints(accused_id);
```

---

## 8. OTP_Verifications Table

**Purpose:** Temporary OTP storage for verification

```sql
CREATE TABLE otp_verifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL,
    otp_code VARCHAR(6) NOT NULL,
    purpose VARCHAR(20) NOT NULL CHECK (purpose IN ('registration', 'login', 'password_reset')),
    is_verified BOOLEAN DEFAULT FALSE,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**
```sql
CREATE INDEX idx_otp_email ON otp_verifications(email);
CREATE INDEX idx_otp_expires ON otp_verifications(expires_at);
```

**Auto-cleanup (PostgreSQL):**
```sql
-- Delete expired OTPs older than 1 hour
DELETE FROM otp_verifications WHERE expires_at < NOW() - INTERVAL '1 hour';
```

---

## Relationships Diagram

```
users (1) ----< (M) bookings
users (1) ----< (M) rides (as driver)
users (1) ----< (M) ratings (as rated_by)
users (1) ----< (M) ratings (as rated_to)
users (1) ----< (M) complaints (as complainant)
users (1) ----< (M) complaints (as accused)
users (1) ---- (1) driver_profiles

routes (1) ----< (M) rides

rides (1) ----< (M) bookings
rides (1) ----< (M) ratings
rides (1) ----< (M) complaints
```

---

## Key Constraints & Business Rules

### 1. User Registration
- Email must end with @geu.ac.in or @gehu.ac.in
- Phone must be unique
- College ID must be unique

### 2. Driver Verification
- Cannot create rides until documents verified
- DL and Insurance must not be expired

### 3. Ride Creation
- Max 4 seats per ride
- Cannot create ride in the past
- Price must be reasonable (₹10-₹100 per seat)

### 4. Booking Rules
- Cannot book own ride
- Cannot book if seats unavailable
- Cannot book same ride twice
- Must verify face before ride starts

### 5. Rating Rules
- Can only rate after ride completion
- Can rate only once per ride
- Both driver and rider can rate each other

### 6. Complaint Rules
- Can only complain about users in same ride
- Must provide description

---

## Database Triggers

### 1. Update Available Seats on Booking
```sql
CREATE OR REPLACE FUNCTION update_available_seats()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.booking_status = 'confirmed' THEN
        UPDATE rides 
        SET available_seats = available_seats - NEW.seats_booked
        WHERE id = NEW.ride_id;
    ELSIF OLD.booking_status = 'confirmed' AND NEW.booking_status = 'cancelled' THEN
        UPDATE rides 
        SET available_seats = available_seats + OLD.seats_booked
        WHERE id = NEW.ride_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER booking_seats_trigger
AFTER INSERT OR UPDATE ON bookings
FOR EACH ROW EXECUTE FUNCTION update_available_seats();
```

### 2. Update Driver Average Rating
```sql
CREATE OR REPLACE FUNCTION update_driver_rating()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE driver_profiles
    SET average_rating = (
        SELECT AVG(rating)::DECIMAL(3,2)
        FROM ratings
        WHERE rated_to = NEW.rated_to
    )
    WHERE user_id = NEW.rated_to;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER rating_update_trigger
AFTER INSERT ON ratings
FOR EACH ROW EXECUTE FUNCTION update_driver_rating();
```

---

## Sample Queries

### Find Available Rides
```sql
SELECT r.*, u.name as driver_name, rt.route_name, dp.average_rating
FROM rides r
JOIN users u ON r.driver_id = u.id
JOIN routes rt ON r.route_id = rt.id
JOIN driver_profiles dp ON u.id = dp.user_id
WHERE r.route_id = 'route-uuid'
  AND r.ride_date = '2024-01-15'
  AND r.status = 'scheduled'
  AND r.available_seats > 0
ORDER BY r.time_slot;
```

### Get User Ride History
```sql
SELECT r.*, rt.route_name, u.name as driver_name, b.booking_status
FROM bookings b
JOIN rides r ON b.ride_id = r.id
JOIN routes rt ON r.route_id = rt.id
JOIN users u ON r.driver_id = u.id
WHERE b.rider_id = 'user-uuid'
ORDER BY r.ride_date DESC, r.time_slot DESC;
```

### Get Driver Statistics
```sql
SELECT 
    u.name,
    dp.total_rides,
    dp.average_rating,
    COUNT(DISTINCT b.id) as total_bookings,
    SUM(b.total_amount) as total_earnings
FROM users u
JOIN driver_profiles dp ON u.id = dp.user_id
LEFT JOIN rides r ON u.id = r.driver_id
LEFT JOIN bookings b ON r.id = b.ride_id AND b.booking_status = 'completed'
WHERE u.id = 'driver-uuid'
GROUP BY u.id, u.name, dp.total_rides, dp.average_rating;
```

---

## Performance Optimization

### 1. Indexes (Already defined above)
### 2. Partitioning (Future)
- Partition rides table by date
- Partition bookings table by date

### 3. Caching Strategy
- Cache active routes
- Cache user profiles
- Cache driver ratings

---

## Backup Strategy

```bash
# Daily backup
pg_dump -U postgres eraride_db > backup_$(date +%Y%m%d).sql

# Restore
psql -U postgres eraride_db < backup_20240115.sql
```

---

## Migration Plan

**Phase 1:** Core tables (users, routes, rides, bookings)
**Phase 2:** Safety tables (ratings, complaints)
**Phase 3:** Optimization (indexes, triggers)
**Phase 4:** Advanced features (face_embedding, analytics)
