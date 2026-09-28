from fastapi import APIRouter

from app.imports.fit.router import router as fit_router

router = APIRouter()

router.include_router(fit_router)