from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database.repository import Repository
from app.workouts.models import LapDBO, WorkoutDBO


class WorkoutRepository(Repository[WorkoutDBO]):
    def __init__(self, session: Session):
        super().__init__(session=session, model=WorkoutDBO)

    def get_with_details(self, workout_id: int) -> WorkoutDBO | None:
        statement = (
            select(WorkoutDBO)
            .options(
                selectinload(WorkoutDBO.laps).selectinload(LapDBO.segments)
            )
            .where(WorkoutDBO.id == workout_id)
        )

        return self._session.scalar(statement)

    def get_latest(self, limit: int, offset: int) -> list[WorkoutDBO]:
        statement = (
            select(WorkoutDBO)
            .order_by(WorkoutDBO.started_at.desc())
            .offset(offset)
            .limit(limit)
        )

        return list(self._session.scalars(statement))
