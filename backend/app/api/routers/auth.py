from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.rate_limit import RateLimit
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.session import get_db
from app.models import User
from app.schemas.auth import LoginRequest, OTPRequest, OTPVerifyRequest, RegisterRequest, TokenResponse
from app.services.otp_service import generate_otp, verify_otp, was_otp_verified

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/otp/request', dependencies=[RateLimit])
async def request_otp(payload: OTPRequest):
    settings = get_settings()
    domain = payload.email.split('@')[-1].lower()
    if domain not in settings.email_domains:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Only university email allowed')
    await generate_otp(payload.email)
    return {'message': 'OTP sent (MVP: logged in backend console)'}


@router.post('/otp/verify', dependencies=[RateLimit])
async def verify_otp_code(payload: OTPVerifyRequest):
    ok = await verify_otp(payload.email, payload.otp)
    if not ok:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid or expired OTP')
    return {'message': 'OTP verified'}


@router.post('/register', response_model=TokenResponse, dependencies=[RateLimit])
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    if not await was_otp_verified(payload.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Verify OTP before registration')

    existing = await db.execute(select(User).where(User.email == payload.email.lower()))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')

    user = User(
        email=payload.email.lower(),
        full_name=payload.full_name,
        password_hash=get_password_hash(payload.password),
        role=payload.role,
        phone=payload.phone,
        section=payload.section,
        year=payload.year,
        is_email_verified=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token = create_access_token(str(user.id), user.role.value)
    return TokenResponse(access_token=token, role=user.role, user_id=user.id)


@router.post('/login', response_model=TokenResponse, dependencies=[RateLimit])
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == payload.email.lower()))
    user = result.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')

    token = create_access_token(str(user.id), user.role.value)
    return TokenResponse(access_token=token, role=user.role, user_id=user.id)
