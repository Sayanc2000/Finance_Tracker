from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from starlette.middleware.base import BaseHTTPMiddleware

from app import models
from app.database import engine
from app.routers import auth, entries, user
from app.schemas import DefaultResponse
from app.utils.middleware import add_process_time_header

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Frugal")

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(entries.router)

app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://redis:6379")
    await redis.ping()
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.get("/", response_model=DefaultResponse)
def root():
    return {"message": "Hello World"}


@app.get("/health", response_model=DefaultResponse)
def health():
    return {"message": "OK"}
