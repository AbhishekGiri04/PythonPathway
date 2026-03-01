from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.security import decode_token
from app.db.redis_client import redis_client
from app.db.session import SessionLocal, get_db
from app.models import Booking, BookingStatus, ChatMessage, ChatRoom, Ride, User
from app.schemas.chat import ChatMessageCreate, ChatMessageOut
from app.services.chat_manager import chat_manager

router = APIRouter(prefix='/chat', tags=['chat'])


async def _user_has_room_access(db: AsyncSession, user_id: int, room_id: int) -> bool:
    room_result = await db.execute(select(ChatRoom).where(ChatRoom.id == room_id))
    room = room_result.scalar_one_or_none()
    if not room:
        return False

    ride_result = await db.execute(select(Ride).where(Ride.id == room.ride_id))
    ride = ride_result.scalar_one_or_none()
    if not ride:
        return False

    if ride.driver_id == user_id:
        return True

    booking_result = await db.execute(
        select(Booking).where(
            Booking.ride_id == ride.id,
            Booking.rider_id == user_id,
            Booking.status == BookingStatus.BOOKED,
        )
    )
    return booking_result.scalar_one_or_none() is not None


@router.post('/room/{ride_id}')
async def create_or_get_room(
    ride_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    ride_result = await db.execute(select(Ride).where(Ride.id == ride_id))
    ride = ride_result.scalar_one_or_none()
    if not ride:
        raise HTTPException(status_code=404, detail='Ride not found')

    if current_user.id != ride.driver_id:
        booking_result = await db.execute(
            select(Booking).where(
                Booking.ride_id == ride_id,
                Booking.rider_id == current_user.id,
                Booking.status == BookingStatus.BOOKED,
            )
        )
        if not booking_result.scalar_one_or_none():
            raise HTTPException(status_code=403, detail='No access to this room')

    room_result = await db.execute(select(ChatRoom).where(ChatRoom.ride_id == ride_id))
    room = room_result.scalar_one_or_none()
    if not room:
        room = ChatRoom(ride_id=ride_id)
        db.add(room)
        await db.commit()
        await db.refresh(room)
    return {'room_id': room.id}


@router.get('/room/{room_id}/messages', response_model=list[ChatMessageOut])
async def messages(room_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not await _user_has_room_access(db, current_user.id, room_id):
        raise HTTPException(status_code=403, detail='No room access')

    result = await db.execute(select(ChatMessage).where(ChatMessage.room_id == room_id).order_by(ChatMessage.created_at.desc()).limit(100))
    return list(reversed(result.scalars().all()))


@router.post('/message', response_model=ChatMessageOut)
async def post_message(
    payload: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not await _user_has_room_access(db, current_user.id, payload.room_id):
        raise HTTPException(status_code=403, detail='No room access')

    message = ChatMessage(room_id=payload.room_id, sender_id=current_user.id, message=payload.message)
    db.add(message)
    await db.commit()
    await db.refresh(message)

    await chat_manager.broadcast(
        payload.room_id,
        {
            'id': message.id,
            'room_id': message.room_id,
            'sender_id': message.sender_id,
            'message': message.message,
            'created_at': str(message.created_at),
        },
    )
    return message


@router.websocket('/ws/{room_id}')
async def websocket_chat(websocket: WebSocket, room_id: int, token: str = Query(...)):
    try:
        payload = decode_token(token)
        user_id = int(payload.get('sub'))
    except Exception:
        await websocket.close(code=1008)
        return

    async with SessionLocal() as db:
        if not await _user_has_room_access(db, user_id, room_id):
            await websocket.close(code=1008)
            return

    await redis_client.setex(f'presence:user:{user_id}', 60, 'online')
    await chat_manager.connect(room_id, websocket)

    try:
        while True:
            text = await websocket.receive_text()
            if text == '__ping__':
                await redis_client.setex(f'presence:user:{user_id}', 60, 'online')
                continue
            async with SessionLocal() as db:
                msg = ChatMessage(room_id=room_id, sender_id=user_id, message=text)
                db.add(msg)
                await db.commit()
                await db.refresh(msg)
            await chat_manager.broadcast(
                room_id,
                {
                    'id': msg.id,
                    'room_id': room_id,
                    'sender_id': user_id,
                    'message': text,
                    'created_at': str(msg.created_at),
                },
            )
    except WebSocketDisconnect:
        chat_manager.disconnect(room_id, websocket)
        await redis_client.delete(f'presence:user:{user_id}')
