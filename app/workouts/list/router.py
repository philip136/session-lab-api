from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.workouts.list.request import WorkoutListRequest
from app.workouts.list.response import WorkoutListResponse
from app.workouts.service import WorkoutServiceDep

router = APIRouter()


@router.get(
    "/",
    response_model=WorkoutListResponse,
    status_code=status.HTTP_200_OK,
)
def get_workouts(
    request: Annotated[WorkoutListRequest, Depends()],
    service: WorkoutServiceDep,
) -> WorkoutListResponse:
    return service.get_list(request)
