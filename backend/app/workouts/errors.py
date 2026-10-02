from backend.app.errors import NotFoundError


class WorkoutNotFoundError(NotFoundError):
    code: str = "WORKOUT_NOT_FOUND"
    message: str = "Workout was not found."

