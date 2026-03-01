from fastapi import APIRouter

from app.api.routers import admin, auth, bookings, chat, complaints, payments, rides, users

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(rides.router)
api_router.include_router(bookings.router)
api_router.include_router(complaints.router)
api_router.include_router(payments.router)
api_router.include_router(chat.router)
api_router.include_router(admin.router)
