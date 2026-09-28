from fastapi import APIRouter

from app.workouts.get.router import router as get_router
from app.workouts.list.router import router as list_router

router = APIRouter()

router.include_router(get_router)
router.include_router(list_router)