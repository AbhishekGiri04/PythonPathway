from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.redis_client import redis_client
from app.models import Booking, BookingStatus, Ride, RideStatus
from app.services.cache_service import invalidate_ride_list_cache


async def create_booking_with_lock(db: AsyncSession, ride_id: int, rider_id: int, seats_booked: int) -> Booking:
    lock_key = f'ride_lock:{ride_id}'
    lock = redis_client.lock(lock_key, timeout=8, blocking_timeout=3)

    async with lock:
        ride_result = await db.execute(
            select(Ride).where(and_(Ride.id == ride_id, Ride.status == RideStatus.OPEN)).with_for_update()
        )
        ride = ride_result.scalar_one_or_none()
        if not ride:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ride not found')
        if ride.available_seats < seats_booked:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not enough seats available')

        existing_result = await db.execute(
            select(Booking).where(
                and_(Booking.ride_id == ride_id, Booking.rider_id == rider_id, Booking.status == BookingStatus.BOOKED)
            )
        )
        if existing_result.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You already booked this ride')

        ride.available_seats -= seats_booked
        booking = Booking(ride_id=ride_id, rider_id=rider_id, seats_booked=seats_booked, status=BookingStatus.BOOKED)
        db.add(booking)
        await db.commit()
        await db.refresh(booking)

    await invalidate_ride_list_cache()
    return booking


async def cancel_booking(db: AsyncSession, booking: Booking) -> Booking:
    if booking.status == BookingStatus.CANCELLED:
        return booking

    ride_result = await db.execute(select(Ride).where(Ride.id == booking.ride_id).with_for_update())
    ride = ride_result.scalar_one_or_none()
    if not ride:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ride not found')

    booking.status = BookingStatus.CANCELLED
    ride.available_seats += booking.seats_booked
    await db.commit()
    await db.refresh(booking)
    await invalidate_ride_list_cache()
    return booking
