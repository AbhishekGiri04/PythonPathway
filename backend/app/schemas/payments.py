from datetime import datetime

from pydantic import BaseModel, Field

from app.models import PaymentStatus


class PaymentCreate(BaseModel):
    booking_id: int | None = None
    amount: float = Field(gt=0)
    currency: str = 'inr'
    payment_type: str = 'cash'


class PaymentOut(BaseModel):
    id: int
    booking_id: int | None
    amount: float
    currency: str
    status: PaymentStatus
    payment_type: str
    stripe_payment_intent_id: str | None
    created_at: datetime

    class Config:
        from_attributes = True
