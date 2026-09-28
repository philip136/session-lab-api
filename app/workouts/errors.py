class WorkoutNotFoundError(Exception):
    def __init__(self, workout_id: int):
        self.workout_id = workout_id
        super().__init__(f"Workout {workout_id} not found")
