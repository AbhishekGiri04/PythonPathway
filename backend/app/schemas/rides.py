from datetime import datetime

from pydantic import BaseModel, Field

from app.models import RideStatus


class RideCreate(BaseModel):
    from_area: str
    to_campus: str
    departure_time: datetime
    total_seats: int = Field(gt=0, le=8)
    price_per_seat: float = Field(ge=0)


class RideOut(BaseModel):
    id: int
    driver_id: int
    from_area: str
    to_campus: str
    departure_time: datetime
    available_seats: int
    total_seats: int
    price_per_seat: float
    status: RideStatus

    class Config:
        from_attributes = True
