import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Literal
from uuid import UUID

from arq.jobs import SerializationError
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from redis.exceptions import RedisError

from backend.lib.enque import enqueue_task
from backend.lib.exceptions import ConfigError
from backend.lib.redis_client import close_redis, get_arq_pool

# Using this line logger output also includ ei the file path.
# As "__name__" becomes file path. 
logger = logging.getLogger(__name__)


# 1. Mentioning the thigngs to start and end when application starts and ends. 
# async.......: used to starts up and close when app dies.
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:   
        await get_arq_pool()
    except (RedisError, OSError, asyncio.TimeoutError):
        logger.warning("Redis unavailable on startup; will retry when handling requests")
    yield
    await close_redis()


app = FastAPI(lifespan=lifespan)


# 2. Adding redis errors Listneres
@app.exception_handler(RedisError)
@app.exception_handler(OSError)
@app.exception_handler(asyncio.TimeoutError)
async def redis_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Redis failure on %s", request.url.path)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "Redis service unavailable"},
    )


# 3. Adding redis exceptions listners. 
@app.exception_handler(SerializationError)
async def serialization_error_handler(request: Request, exc: SerializationError) -> JSONResponse:
    logger.exception("Job serialization error on %s", request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Failed to serialize job payload"},
    )


@app.exception_handler(ConfigError)
async def config_error_handler(request: Request, exc: ConfigError) -> JSONResponse:
    logger.exception("Configuration error on %s", request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc)},
    )


# 4. starting end point. 

# BaseModel also validates the data comming. 
class CreateTaskRequest(BaseModel):
    user_id: UUID
    task: str = Field(min_length=1, max_length=500)


class CreateTaskResponse(BaseModel):
    job_id: str | None
    status: Literal["queued", "duplicate"]


# 4. Starting an endpoint: takes the task and enque it. 
@app.post(
    "/tasks",
    response_model=CreateTaskResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def create_task(payload: CreateTaskRequest) -> CreateTaskResponse:
    job = await enqueue_task(user_id=str(payload.user_id), task=payload.task)

    return CreateTaskResponse(
        job_id=job.job_id if job else None,
        status="queued" if job else "duplicate",
    )


