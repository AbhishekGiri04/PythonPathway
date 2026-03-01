from datetime import datetime

from pydantic import BaseModel

from app.models import Role, UserStatus, VehicleStatus


class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    role: Role
    is_email_verified: bool
    is_driver_verified: bool
    verified_badge: bool
    status: UserStatus
    wallet_balance: float

    class Config:
        from_attributes = True


class VehicleUpsert(BaseModel):
    vehicle_type: str
    vehicle_number: str
    model: str
    color: str
    dl_url: str
    rc_url: str
    insurance_url: str


class VehicleOut(BaseModel):
    id: int
    driver_id: int
    vehicle_type: str
    vehicle_number: str
    model: str
    color: str
    verification_status: VehicleStatus
    verification_notes: str | None
    created_at: datetime

    class Config:
        from_attributes = True
