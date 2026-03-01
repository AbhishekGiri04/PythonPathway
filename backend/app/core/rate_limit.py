from fastapi import Depends, HTTPException, Request, status

from app.core.config import get_settings
from app.db.redis_client import redis_client


async def rate_limit(request: Request) -> None:
    settings = get_settings()
    ip = request.client.host if request.client else 'unknown'
    key = f'ratelimit:{ip}'
    current = await redis_client.incr(key)
    if current == 1:
        await redis_client.expire(key, 60)
    if current > settings.rate_limit_per_minute:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail='Rate limit exceeded')


RateLimit = Depends(rate_limit)
