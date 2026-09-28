from collections.abc import Callable
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.db import get_session

DbSession = Annotated[Session, Depends(get_session)]


def session_dep[T](dependency_type: type[T]) -> Callable[..., T]:
    def dependency(session: DbSession) -> T:
        return dependency_type(session)

    return dependency
