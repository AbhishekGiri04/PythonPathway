from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_roles
from app.db.session import get_db
from app.models import Role, User, UserStatus, Vehicle, VehicleStatus
from app.schemas.users import UserOut, VehicleOut

router = APIRouter(prefix='/admin', tags=['admin'])


@router.get('/drivers/pending', response_model=list[VehicleOut])
async def pending_drivers(_: User = Depends(require_roles(Role.ADMIN)), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Vehicle).where(Vehicle.verification_status == VehicleStatus.PENDING))
    return result.scalars().all()


@router.patch('/drivers/{driver_id}/verify', response_model=VehicleOut)
async def verify_driver(
    driver_id: int,
    approved: bool,
    notes: str = '',
    _: User = Depends(require_roles(Role.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    vehicle_result = await db.execute(select(Vehicle).where(Vehicle.driver_id == driver_id))
    vehicle = vehicle_result.scalar_one_or_none()
    user_result = await db.execute(select(User).where(User.id == driver_id))
    user = user_result.scalar_one_or_none()
    if not vehicle or not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Driver vehicle not found')

    vehicle.verification_status = VehicleStatus.APPROVED if approved else VehicleStatus.REJECTED
    vehicle.verification_notes = notes
    user.is_driver_verified = approved
    user.verified_badge = approved
    await db.commit()
    await db.refresh(vehicle)
    return vehicle


@router.patch('/users/{user_id}/suspend', response_model=UserOut)
async def suspend_user(
    user_id: int,
    suspend: bool,
    _: User = Depends(require_roles(Role.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    user.status = UserStatus.SUSPENDED if suspend else UserStatus.ACTIVE
    await db.commit()
    await db.refresh(user)
    return user
