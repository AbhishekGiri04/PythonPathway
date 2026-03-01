from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models import Complaint, Role, User
from app.schemas.complaints import ComplaintCreate, ComplaintOut, ComplaintUpdate

router = APIRouter(prefix='/complaints', tags=['complaints'])


@router.post('', response_model=ComplaintOut)
async def create_complaint(
    payload: ComplaintCreate,
    current_user: User = Depends(require_roles(Role.TEACHER, Role.RIDER, Role.DRIVER)),
    db: AsyncSession = Depends(get_db),
):
    complaint = Complaint(complainant_id=current_user.id, **payload.model_dump())
    db.add(complaint)
    await db.commit()
    await db.refresh(complaint)
    return complaint


@router.get('/mine', response_model=list[ComplaintOut])
async def my_complaints(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Complaint).where(Complaint.complainant_id == current_user.id))
    return result.scalars().all()


@router.get('', response_model=list[ComplaintOut])
async def list_complaints(_: User = Depends(require_roles(Role.ADMIN)), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Complaint).order_by(Complaint.created_at.desc()).limit(300))
    return result.scalars().all()


@router.patch('/{complaint_id}', response_model=ComplaintOut)
async def update_complaint(
    complaint_id: int,
    payload: ComplaintUpdate,
    _: User = Depends(require_roles(Role.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Complaint).where(Complaint.id == complaint_id))
    complaint = result.scalar_one_or_none()
    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Complaint not found')

    complaint.status = payload.status
    complaint.admin_notes = payload.admin_notes
    await db.commit()
    await db.refresh(complaint)
    return complaint
