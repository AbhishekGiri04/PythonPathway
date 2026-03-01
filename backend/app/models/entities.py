from datetime import datetime
from enum import Enum

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Enum as SQLEnum,
    Float,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Role(str, Enum):
    DRIVER = 'driver'
    RIDER = 'rider'
    TEACHER = 'teacher'
    ADMIN = 'admin'


class UserStatus(str, Enum):
    ACTIVE = 'active'
    SUSPENDED = 'suspended'


class VehicleStatus(str, Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'


class RideStatus(str, Enum):
    OPEN = 'open'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'


class BookingStatus(str, Enum):
    BOOKED = 'booked'
    CANCELLED = 'cancelled'


class PaymentStatus(str, Enum):
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'


class ComplaintStatus(str, Enum):
    OPEN = 'open'
    IN_REVIEW = 'in_review'
    RESOLVED = 'resolved'
    REJECTED = 'rejected'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(120))
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[Role] = mapped_column(SQLEnum(Role), index=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    section: Mapped[str | None] = mapped_column(String(20), nullable=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_phone_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_face_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_driver_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verified_badge: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[UserStatus] = mapped_column(SQLEnum(UserStatus), default=UserStatus.ACTIVE, index=True)
    wallet_balance: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    vehicle: Mapped['Vehicle'] = relationship(back_populates='driver', uselist=False)
    rides: Mapped[list['Ride']] = relationship(back_populates='driver')


class Vehicle(Base):
    __tablename__ = 'vehicles'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), unique=True, index=True)
    vehicle_type: Mapped[str] = mapped_column(String(60))
    vehicle_number: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    model: Mapped[str] = mapped_column(String(80))
    color: Mapped[str] = mapped_column(String(40))
    dl_url: Mapped[str] = mapped_column(String(255))
    rc_url: Mapped[str] = mapped_column(String(255))
    insurance_url: Mapped[str] = mapped_column(String(255))
    verification_status: Mapped[VehicleStatus] = mapped_column(SQLEnum(VehicleStatus), default=VehicleStatus.PENDING, index=True)
    verification_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    driver: Mapped[User] = relationship(back_populates='vehicle')


class Ride(Base):
    __tablename__ = 'rides'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    from_area: Mapped[str] = mapped_column(String(120), index=True)
    to_campus: Mapped[str] = mapped_column(String(120), index=True)
    departure_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    available_seats: Mapped[int] = mapped_column(Integer)
    total_seats: Mapped[int] = mapped_column(Integer)
    price_per_seat: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    status: Mapped[RideStatus] = mapped_column(SQLEnum(RideStatus), default=RideStatus.OPEN, index=True)
    meta: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    driver: Mapped[User] = relationship(back_populates='rides')
    bookings: Mapped[list['Booking']] = relationship(back_populates='ride')


class Booking(Base):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ride_id: Mapped[int] = mapped_column(ForeignKey('rides.id', ondelete='CASCADE'), index=True)
    rider_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    seats_booked: Mapped[int] = mapped_column(Integer)
    status: Mapped[BookingStatus] = mapped_column(SQLEnum(BookingStatus), default=BookingStatus.BOOKED, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    ride: Mapped[Ride] = relationship(back_populates='bookings')

    __table_args__ = (UniqueConstraint('ride_id', 'rider_id', 'status', name='uq_booking_active'),)


class Payment(Base):
    __tablename__ = 'payments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    booking_id: Mapped[int | None] = mapped_column(ForeignKey('bookings.id', ondelete='SET NULL'), nullable=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    stripe_payment_intent_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    amount: Mapped[float] = mapped_column(Numeric(10, 2))
    currency: Mapped[str] = mapped_column(String(8), default='inr')
    status: Mapped[PaymentStatus] = mapped_column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING, index=True)
    payment_type: Mapped[str] = mapped_column(String(30), default='cash')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class WalletTransaction(Base):
    __tablename__ = 'wallet_transactions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    amount: Mapped[float] = mapped_column(Numeric(10, 2))
    txn_type: Mapped[str] = mapped_column(String(30))
    reference: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Complaint(Base):
    __tablename__ = 'complaints'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    complainant_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    accused_user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    ride_id: Mapped[int | None] = mapped_column(ForeignKey('rides.id', ondelete='SET NULL'), nullable=True, index=True)
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[ComplaintStatus] = mapped_column(SQLEnum(ComplaintStatus), default=ComplaintStatus.OPEN, index=True)
    admin_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ChatRoom(Base):
    __tablename__ = 'chat_rooms'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ride_id: Mapped[int] = mapped_column(ForeignKey('rides.id', ondelete='CASCADE'), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ChatMessage(Base):
    __tablename__ = 'chat_messages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('chat_rooms.id', ondelete='CASCADE'), index=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)


Index('ix_ride_status_driver', Ride.status, Ride.driver_id)
Index('ix_booking_ride_status', Booking.ride_id, Booking.status)
Index('ix_complaint_status_created', Complaint.status, Complaint.created_at)
