import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.errors.handlers import register_exception_handlers
from backend.api.fit.router import router as fit_router
from backend.api.workouts.router import router as workout_router
from backend.infra.config.settings import settings
from backend.infra.database.db import close_db, init_db

routers = [
    fit_router,
    workout_router
]

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("SessionLab starting")

    await init_db()

    try:
        yield
    finally:
        await close_db()
        logger.info("SessionLab stopped")


app = FastAPI(title="SessionLab", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for route in routers:
    app.include_router(route)

register_exception_handlers(app)
