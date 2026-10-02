from typing import Annotated

from fastapi import APIRouter, Depends, status

from backend.api.workouts.schemas.details import WorkoutDetailsRequest, WorkoutDetailsResponse
from backend.app.workouts.service import WorkoutService

router = APIRouter(prefix="/workouts", tags=["Workouts"])

@router.get(
    "/{workout_id}",
    response_model=WorkoutDetailsResponse,
    status_code=status.HTTP_200_OK
)
async def get_details(
    workout_id: int,
    service: Annotated[WorkoutService, Depends()]
) -> WorkoutDetailsResponse:
    request = WorkoutDetailsRequest(workout_id=workout_id)
    return await service.get(request)

