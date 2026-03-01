from datetime import datetime

from pydantic import BaseModel


class ChatMessageCreate(BaseModel):
    room_id: int
    message: str


class ChatMessageOut(BaseModel):
    id: int
    room_id: int
    sender_id: int
    message: str
    created_at: datetime

    class Config:
        from_attributes = True
