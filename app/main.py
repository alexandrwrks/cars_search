from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn

from fastapi import FastAPI

from app.routers import router
from scripts.scheduler import scheduler
from services.cache.redis import redis


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    scheduler.start()

    yield

    scheduler.shutdown()


app = FastAPI(
    lifespan=lifespan,
    title="CarsAPI",
    description="API for cars",
    version="1.0.1",
    contact={
        "name": "Alexeyev Alexandr",
        "email": "alexandrwrks@gmail.com",
        "url": "https://www.alexandrwrks.com",
    },

)


app.include_router(router)

@app.on_event("shutdown")
async def shutdown_event():
    await redis.aclose()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)