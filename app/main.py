from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from redis import asyncio as aioredis
from fastapi_cache.backends.redis import RedisBackend
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from starlette.staticfiles import StaticFiles
from app.bookings.router import router as booking_router
from app.images.router import router as image_router
from app.users.router import  auth_router, user_router
from app.hotels.router import router as hotels_router
from app.pages.router import  router as router_page



@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
app = FastAPI(lifespan=lifespan)



app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(booking_router)
app.include_router(hotels_router)
app.include_router(router_page)
app.include_router(image_router)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "Set-Cookie",
                   "Access-Control-Allow-Origin",
                   "Access-Control-Allow-Headers"],
)




