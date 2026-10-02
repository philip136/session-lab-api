from typing import Annotated

from fastapi.params import Depends

from backend.api.workouts.schemas.details import WorkoutDetailsRequest, WorkoutDetailsResponse
from backend.app.workouts.errors import WorkoutNotFoundError
from backend.infra.database.repos.workout import WorkoutRepo


class WorkoutService:
    def __init__(self, repo: Annotated[WorkoutRepo, Depends()]):
        self._repo = repo

    async def get(self, req: WorkoutDetailsRequest) -> WorkoutDetailsResponse:
        workout = await self._repo.get_details(req.workout_id)

        if workout is None:
            raise WorkoutNotFoundError(req.workout_id)

        return WorkoutDetailsResponse.model_validate(workout)

