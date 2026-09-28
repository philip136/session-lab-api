from fastapi import APIRouter, HTTPException, status

from app.workouts.errors import WorkoutNotFoundError
from app.workouts.get.request import WorkoutGetRequest
from app.workouts.get.response import WorkoutGetResponse
from app.workouts.service import WorkoutServiceDep

router = APIRouter()


@router.get(
    "/{workout_id}",
    response_model=WorkoutGetResponse,
    status_code=status.HTTP_200_OK,
)
def get_workout(
    workout_id: int,
    service: WorkoutServiceDep,
) -> WorkoutGetResponse:
    request = WorkoutGetRequest(workout_id=workout_id)

    try:
        return service.get(request)
    except WorkoutNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
