import asyncio

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


async def get_reddit_top_async(subreddit: str, data: dict) -> None:  # 2
    async with httpx.AsyncClient() as client:  # 3
        response = await client.get(  # 4
            f"https://www.reddit.com/r/{subreddit}/top.json?sort=top&t=day&limit=5",
            headers={"User-agent": "recipe bot 0.1"},
        )

    subreddit_recipes = response.json()
    subreddit_data = []
    for entry in subreddit_recipes["data"]["children"]:
        score = entry["data"]["score"]
        title = entry["data"]["title"]
        link = entry["data"]["url"]
        subreddit_data.append(f"{str(score)}: {title} ({link})")
    data[subreddit] = subreddit_data


@app.get("/test1")
async def test():
    data: dict = {}

    await asyncio.gather(  # 5
        get_reddit_top_async("recipes", data),
        get_reddit_top_async("easyrecipes", data),
        get_reddit_top_async("TopSecretRecipes", data),
    )

    return data


def get_reddit_top(subreddit: str, data: dict) -> None:
    response = httpx.get(
        f"https://www.reddit.com/r/{subreddit}/top.json?sort=top&t=day&limit=5",
        headers={"User-agent": "recipe bot 0.1"},
    )  # 2
    subreddit_recipes = response.json()
    subreddit_data = []
    for entry in subreddit_recipes["data"]["children"]:
        score = entry["data"]["score"]
        title = entry["data"]["title"]
        link = entry["data"]["url"]
        subreddit_data.append(f"{str(score)}: {title} ({link})")
    data[subreddit] = subreddit_data


@app.get("/test2")
def fetch_ideas() -> dict:
    data: dict = {}  # 3
    get_reddit_top("recipes", data)
    get_reddit_top("easyrecipes", data)
    get_reddit_top("TopSecretRecipes", data)

    return data
