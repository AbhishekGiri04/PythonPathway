from datetime import datetime

from pydantic import BaseModel, Field

from app.models import BookingStatus


class BookingCreate(BaseModel):
    ride_id: int
    seats_booked: int = Field(gt=0, le=4)


class BookingOut(BaseModel):
    id: int
    ride_id: int
    rider_id: int
    seats_booked: int
    status: BookingStatus
    created_at: datetime

    class Config:
        from_attributes = True
