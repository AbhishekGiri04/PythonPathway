import asyncio

from sqlalchemy import select

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models import Role, User


async def seed() -> None:
    async with SessionLocal() as db:
        result = await db.execute(select(User).where(User.email == 'admin@gehu.ac.in'))
        user = result.scalar_one_or_none()
        if user:
            print('Admin already exists: admin@gehu.ac.in')
            return
        admin = User(
            email='admin@gehu.ac.in',
            full_name='EraRide Admin',
            password_hash=get_password_hash('Admin@123'),
            role=Role.ADMIN,
            is_email_verified=True,
            is_driver_verified=True,
            verified_badge=True,
        )
        db.add(admin)
        await db.commit()
        print('Seeded admin user: admin@gehu.ac.in / Admin@123')


if __name__ == '__main__':
    asyncio.run(seed())
