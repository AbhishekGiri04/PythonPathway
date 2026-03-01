from datetime import datetime

from pydantic import BaseModel

from app.models import ComplaintStatus


class ComplaintCreate(BaseModel):
    accused_user_id: int | None = None
    ride_id: int | None = None
    description: str


class ComplaintUpdate(BaseModel):
    status: ComplaintStatus
    admin_notes: str | None = None


class ComplaintOut(BaseModel):
    id: int
    complainant_id: int
    accused_user_id: int | None
    ride_id: int | None
    description: str
    status: ComplaintStatus
    admin_notes: str | None
    created_at: datetime

    class Config:
        from_attributes = True
