from app.db.redis_client import redis_client


async def invalidate_ride_list_cache() -> None:
    cursor = 0
    keys: list[str] = []
    while True:
        cursor, batch = await redis_client.scan(cursor=cursor, match='rides:list:*', count=100)
        keys.extend(batch)
        if cursor == 0:
            break
    if keys:
        await redis_client.delete(*keys)
