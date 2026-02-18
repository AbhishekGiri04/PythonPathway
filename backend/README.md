# EraRide Backend Setup

## Prerequisites
- Python 3.10+
- PostgreSQL 14+
- pip

## Setup Steps

### 1. Create Virtual Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup PostgreSQL Database
```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE eraride_db;

# Create user (optional)
CREATE USER eraride_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE eraride_db TO eraride_user;
```

### 4. Environment Variables
```bash
cp .env.example .env
# Edit .env with your actual credentials
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Server will run at: http://localhost:8000

## API Documentation
Once server is running, visit:
- Admin Panel: http://localhost:8000/admin
- API Root: http://localhost:8000/api/

## Project Structure
```
backend/
├── eraride/              # Main project settings
├── users/                # User authentication & profiles
├── rides/                # Ride management
├── bookings/             # Booking system
├── face_verification/    # AI face verification
├── complaints/           # Complaint system
├── ratings/              # Rating system
└── manage.py
```

## Next Steps
1. ✅ Setup complete
2. ⏳ Create Django apps
3. ⏳ Define models
4. ⏳ Create API endpoints
