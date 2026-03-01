import json

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_roles
from app.core.config import get_settings
from app.db.redis_client import redis_client
from app.db.session import get_db
from app.models import Ride, RideStatus, Role, User
from app.schemas.rides import RideCreate, RideOut
from app.services.cache_service import invalidate_ride_list_cache

router = APIRouter(prefix='/rides', tags=['rides'])


@router.post('', response_model=RideOut)
async def create_ride(
    payload: RideCreate,
    current_user: User = Depends(require_roles(Role.DRIVER)),
    db: AsyncSession = Depends(get_db),
):
    if not current_user.is_driver_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Driver is not verified by admin')

    ride = Ride(
        driver_id=current_user.id,
        from_area=payload.from_area,
        to_campus=payload.to_campus,
        departure_time=payload.departure_time,
        total_seats=payload.total_seats,
        available_seats=payload.total_seats,
        price_per_seat=payload.price_per_seat,
    )
    db.add(ride)
    await db.commit()
    await db.refresh(ride)
    await invalidate_ride_list_cache()
    return ride


@router.get('', response_model=list[RideOut])
async def list_rides(
    from_area: str | None = Query(default=None),
    to_campus: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    settings = get_settings()
    cache_key = f'rides:list:{from_area or "all"}:{to_campus or "all"}'
    cached = await redis_client.get(cache_key)
    if cached:
        return [RideOut(**item) for item in json.loads(cached)]

    filters = [Ride.status == RideStatus.OPEN]
    if from_area:
        filters.append(Ride.from_area.ilike(f'%{from_area}%'))
    if to_campus:
        filters.append(Ride.to_campus.ilike(f'%{to_campus}%'))

    result = await db.execute(select(Ride).where(and_(*filters)).order_by(Ride.departure_time.asc()).limit(200))
    rides = result.scalars().all()
    response = [RideOut.model_validate(ride).model_dump(mode='json') for ride in rides]
    await redis_client.setex(cache_key, settings.ride_cache_ttl_seconds, json.dumps(response, default=str))
    return [RideOut(**item) for item in response]


@router.get('/mine', response_model=list[RideOut])
async def my_rides(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Ride).where(Ride.driver_id == current_user.id).order_by(Ride.departure_time.desc()))
    return result.scalars().all()


@router.patch('/{ride_id}/cancel', response_model=RideOut)
async def cancel_ride(
    ride_id: int,
    current_user: User = Depends(require_roles(Role.DRIVER, Role.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Ride).where(Ride.id == ride_id))
    ride = result.scalar_one_or_none()
    if not ride:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ride not found')
    if current_user.role != Role.ADMIN and ride.driver_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not allowed')

    ride.status = RideStatus.CANCELLED
    await db.commit()
    await db.refresh(ride)
    await invalidate_ride_list_cache()
    return ride
