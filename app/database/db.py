from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config.settings import settings

DEFAULT_DB_PATH = Path("data/sessionlab.db")
DEFAULT_DB_PATH.parent.mkdir(parents=True, exist_ok=True)



class Base(DeclarativeBase):
    pass


engine_options: dict = {
    "pool_pre_ping": True,
}

if settings.database_url.startswith("sqlite"):
    engine_options["connect_args"] = {
        "check_same_thread": False,
    }


engine = create_engine(
    settings.database_url,
    **engine_options,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def get_session() -> Generator[Session]:
    with SessionLocal() as session:
        try:
            yield session
        except Exception:
            session.rollback()
            raise


def init_db() -> None:
    from app.workouts import models  # noqa: F401
    Base.metadata.create_all(engine)
