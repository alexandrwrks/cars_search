from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.routers import routers


@asynccontextmanager
async def lifespan(_: FastAPI):

    yield


app = FastAPI(
    lifespan=lifespan,
    version="1.0.0",
    title="Open Cars API",
    description=
    """
    Open Cars API
    You can use this api with a secret_api_key,
    which allows you to retrieve data
    """,
)

for router in routers:
    app.include_router(router)



if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8001, reload=True)