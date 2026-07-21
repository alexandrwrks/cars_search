from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routers import router
from scripts.scheduler import scheduler
from services.cache.redis import redis
from utils.logger import logger


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    scheduler.start()

    yield

    scheduler.shutdown()
    await redis.aclose()

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


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(
        "Unhandled exception",
        extra={
            "method": request.method,
            "path": request.url.path
        },
    )

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)