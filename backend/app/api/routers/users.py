from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models import Role, User, Vehicle, VehicleStatus
from app.schemas.users import UserOut, VehicleOut, VehicleUpsert

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/me', response_model=UserOut)
async def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put('/me/vehicle', response_model=VehicleOut)
async def upsert_vehicle(
    payload: VehicleUpsert,
    current_user: User = Depends(require_roles(Role.DRIVER)),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Vehicle).where(Vehicle.driver_id == current_user.id))
    vehicle = result.scalar_one_or_none()
    if vehicle:
        for field, value in payload.model_dump().items():
            setattr(vehicle, field, value)
        vehicle.verification_status = VehicleStatus.PENDING
    else:
        vehicle = Vehicle(driver_id=current_user.id, **payload.model_dump())
        db.add(vehicle)

    current_user.is_driver_verified = False
    current_user.verified_badge = False
    await db.commit()
    await db.refresh(vehicle)
    return vehicle


@router.get('/driver/{driver_id}/masked-contact')
async def masked_driver_contact(driver_id: int, db: AsyncSession = Depends(get_db), _: User = Depends(get_current_user)):
    result = await db.execute(select(User).where(User.id == driver_id, User.role == Role.DRIVER))
    driver = result.scalar_one_or_none()
    if not driver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Driver not found')

    phone = driver.phone or '9999999999'
    return {'masked_phone': f"XXXXXX{phone[-4:]}"}
