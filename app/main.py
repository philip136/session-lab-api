import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.logging import configure_logging
from app.config.settings import settings
from app.database.db import init_db
from app.imports.router import router as import_router
from app.workouts.router import router as workout_router

configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("SessionLab starting")
    init_db()
    yield
    logger.info("SessionLab stopped")


app = FastAPI(
    title="SessionLab",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(import_router, prefix="/imports", tags=["Imports"])
app.include_router(workout_router, prefix="/workouts", tags=["Workouts"])
