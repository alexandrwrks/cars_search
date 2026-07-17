from app.routers.v1.cars import router as cars_router
from app.routers.v1.personal import router as personal_router
from app.routers.v1.auth import router as auth_router


routers = [
    cars_router,
    personal_router,
    auth_router,
]