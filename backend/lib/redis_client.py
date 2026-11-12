import asyncio
import logging

from arq import create_pool
from arq.connections import ArqRedis
from redis.exceptions import RedisError

from backend.lib.config import get_redis_settings

logger = logging.getLogger(__name__)

_arq_pool: ArqRedis | None = None
_arq_lock = asyncio.Lock()


# 1. Creates pool of connections.
async def get_arq_pool() -> ArqRedis:
    global _arq_pool
    if _arq_pool is None:
        async with _arq_lock:
            if _arq_pool is None:
                _arq_pool = await create_pool(get_redis_settings())
    return _arq_pool


# 2. Closes all the clients and
async def close_redis() -> None:
    """Close the open ARQ singleton client."""
    global _arq_pool
    if _arq_pool is None:
        return
    try:
        await _arq_pool.aclose()
    except (RedisError, OSError):
        logger.warning("Error closing ARQ client during shutdown", exc_info=True)
    finally:
        _arq_pool = None