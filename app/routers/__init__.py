from fastapi import APIRouter

from app.routers.v1.auth import router as auth_router
from app.routers.v1.cars import router as cars_router
from app.routers.v1.personal import router as personal_router
from app.routers.v1.statistics import router as statistics_router

router = APIRouter()

router.include_router(cars_router, prefix="/v1/cars", tags=["Cars"])
router.include_router(personal_router, prefix="/v1/personal", tags=["Personal"])
router.include_router(auth_router, prefix="/v1/auth", tags=["Auth"])
router.include_router(statistics_router, prefix="/v1/cars/statistics", tags=["Statistics"])