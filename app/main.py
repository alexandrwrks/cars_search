from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn

from fastapi import FastAPI

from app.routers import routers


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    print("Lifespan...")
    yield


app = FastAPI(lifespan=lifespan, title="CarsAPI")

for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)