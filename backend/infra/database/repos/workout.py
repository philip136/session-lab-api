from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.infra.database.entities.workout import LapEntity, WorkoutEntity
from backend.infra.database.repos.repo import Repo


class WorkoutRepo(Repo[WorkoutEntity]):
    _model = WorkoutEntity

    async def get_details(self, workout_id: int) -> WorkoutEntity | None:
        statement = select(self._model).options(
            selectinload(self._model.laps).
            selectinload(LapEntity.segments)
        ).where(self._model.id == workout_id)
        return await self.scalar(statement)

    async def get_latest(self, limit: int, offset: int) -> list[WorkoutEntity]:
        statement = select(self._model).order_by(
            self._model.started_at.desc()
        ).offset(offset).limit(limit)
        return await self.scalars(statement)
