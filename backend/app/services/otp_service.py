import logging
import random

from app.core.config import get_settings
from app.db.redis_client import redis_client

logger = logging.getLogger(__name__)


async def generate_otp(email: str) -> None:
    settings = get_settings()
    otp = str(random.randint(100000, 999999))
    await redis_client.setex(f'otp:{email.lower()}', settings.otp_ttl_seconds, otp)
    logger.info('MVP OTP for %s: %s', email, otp)


async def verify_otp(email: str, otp: str) -> bool:
    key = f'otp:{email.lower()}'
    saved = await redis_client.get(key)
    if saved and saved == otp:
        await redis_client.delete(key)
        await redis_client.setex(f'otp_verified:{email.lower()}', 3600, '1')
        return True
    return False


async def was_otp_verified(email: str) -> bool:
    return bool(await redis_client.get(f'otp_verified:{email.lower()}'))
