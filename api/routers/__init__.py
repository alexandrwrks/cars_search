from api.routers.api_key import router as api_key_router
from api.routers.auth import router as auth_router
from api.routers.cars import router as cars_router

routers = [
    cars_router,
    auth_router,
    api_key_router,
]