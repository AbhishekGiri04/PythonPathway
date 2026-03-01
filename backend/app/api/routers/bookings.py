from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models import Booking, Role, User
from app.schemas.bookings import BookingCreate, BookingOut
from app.services.booking_service import cancel_booking, create_booking_with_lock

router = APIRouter(prefix='/bookings', tags=['bookings'])


@router.post('', response_model=BookingOut)
async def create_booking(
    payload: BookingCreate,
    current_user: User = Depends(require_roles(Role.RIDER, Role.TEACHER)),
    db: AsyncSession = Depends(get_db),
):
    return await create_booking_with_lock(db, payload.ride_id, current_user.id, payload.seats_booked)


@router.get('/mine', response_model=list[BookingOut])
async def my_bookings(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Booking).where(Booking.rider_id == current_user.id).order_by(Booking.created_at.desc()))
    return result.scalars().all()


@router.patch('/{booking_id}/cancel', response_model=BookingOut)
async def cancel_my_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Booking not found')
    if current_user.role != Role.ADMIN and booking.rider_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not allowed')
    return await cancel_booking(db, booking)
