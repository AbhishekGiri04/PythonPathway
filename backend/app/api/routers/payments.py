from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import Payment, PaymentStatus, User
from app.schemas.payments import PaymentCreate, PaymentOut
from app.services.payment_service import create_payment_intent

router = APIRouter(prefix='/payments', tags=['payments'])


@router.post('', response_model=PaymentOut)
async def create_payment(
    payload: PaymentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    intent_id = None
    status = PaymentStatus.PENDING

    if payload.payment_type == 'stripe':
        intent_id = create_payment_intent(payload.amount, metadata={'user_id': str(current_user.id)})
        if intent_id:
            status = PaymentStatus.SUCCESS

    if payload.payment_type == 'cash':
        status = PaymentStatus.SUCCESS

    payment = Payment(
        booking_id=payload.booking_id,
        user_id=current_user.id,
        amount=payload.amount,
        currency=payload.currency,
        payment_type=payload.payment_type,
        stripe_payment_intent_id=intent_id,
        status=status,
    )
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    return payment
