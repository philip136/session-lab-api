import logging
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.deps import session_dep
from app.workouts.errors import WorkoutNotFoundError
from app.workouts.get.request import WorkoutGetRequest
from app.workouts.get.response import WorkoutGetResponse
from app.workouts.list.request import WorkoutListRequest
from app.workouts.list.response import WorkoutListItemResponse, WorkoutListResponse
from app.workouts.repository import WorkoutRepository

logger = logging.getLogger()


class WorkoutService:
    def __init__(self, session: Session):
        self._repo = WorkoutRepository(session)

    def get(self, request: WorkoutGetRequest) -> WorkoutGetResponse:
        workout = self._repo.get_with_details(request.workout_id)

        if workout is None:
            logger.debug(
                "Workout not found: workout_id=%s",
                request.workout_id,
            )
            raise WorkoutNotFoundError(request.workout_id)

        return WorkoutGetResponse.model_validate(workout)

    def get_list(self, request: WorkoutListRequest) -> WorkoutListResponse:
        workouts = self._repo.get_latest(
            limit=request.limit,
            offset=request.offset,
        )

        return WorkoutListResponse(
            items=[
                WorkoutListItemResponse.model_validate(workout)
                for workout in workouts
            ],
            limit=request.limit,
            offset=request.offset,
        )


WorkoutServiceDep = Annotated[
    WorkoutService,
    Depends(session_dep(WorkoutService)),
]
