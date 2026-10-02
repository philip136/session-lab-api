from typing import Annotated

from fastapi.params import Depends
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.infra.database.db import Base, get_session


class Repo[ModelT: Base]:
    _model: type[ModelT]

    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self._session = session

    async def save(self, entity: ModelT) -> ModelT:
        self._session.add(entity)
        await self._session.flush()
        await self._session.commit()
        return entity

    async def get(self, entity_id: int) -> ModelT | None:
        return await self._session.get(self._model, entity_id)

    async def delete(self, entity: ModelT):
        await self._session.delete(entity)

    async def scalar(self, statement: Select[tuple[ModelT]]) -> ModelT | None:
        return await self._session.scalar(statement)

    async def scalars(self, statement: Select[tuple[ModelT]]) -> list[tuple[ModelT]]:
        return list(await self._session.scalars(statement))