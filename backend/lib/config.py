import os
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

from backend.lib.exceptions import ConfigError
from arq.connections import RedisSettings

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


# Builds a imutable list
ALLOWED_REDIS_SCHEMES = frozenset({"redis", "rediss", "unix"})

# 1. Parsing the redis url with error handling. 
def get_redis_url() -> str:
    raw = (os.getenv("REDIS_URL") or "").strip()

    scheme = urlparse(raw).scheme
    if scheme not in ALLOWED_REDIS_SCHEMES:
        raise ConfigError(
            f"Invalid REDIS_URL scheme {scheme!r}; expected one of {sorted(ALLOWED_REDIS_SCHEMES)}"
        )
    return raw 


# 2. Returns 'RedisSetting' parameter.
def get_redis_settings() -> RedisSettings:
    try:
        return RedisSettings.from_dsn(get_redis_url())
    except (RuntimeError, ValueError) as exc:
        raise ConfigError("Invalid Redis DSN configuration") from exc