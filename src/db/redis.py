from redis.asyncio import Redis
from src.config import settings

token_blocklist = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True
)

async def add_to_blocklist(jti: str, expires_at: int=3600):
    """
    Add a token's unique ID (jti) to the Redis blocklist.

    Parameters:
        jti (str): Unique identifier of the token.
        expires_at (int): Time-to-live (TTL) in seconds

    """
    await token_blocklist.set(
        name=jti,
        value="",
        ex=expires_at
    )

async def is_token_blocked(jti: str) -> bool:
    return await token_blocklist.get(jti) is not None
