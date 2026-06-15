from gym_app.models import User, Routine, Routine_Exercise, User_Area_Level
from gym_app.repositories import validation_repo as repo


# --- Validaciones ---
def validate_user_goal(user: User):
    if user.goal_id is None:
        raise ValueError("El usuario no tiene un objetivo definido")


def validate_user_levels(user: User):
    if not repo.user_has_area_levels(user):
        raise ValueError("El usuario no tiene niveles por área asignados")


def validate_available_exercises(exercises: list, required: int):
    if len(exercises) < required:
        raise ValueError("No hay suficientes ejercicios para generar la rutina")

# --- Lógica de negocio ---
def apply_level_to_exercise(routine_exercise: Routine_Exercise, user: User) -> dict:
    exercise = routine_exercise.Exercise_id
    area = exercise.MuscularArea_id
    level = repo.get_user_level_for_area(user, area)

    series = routine_exercise.Series
    reps = routine_exercise.Reps

    if level:
        series = round(series * level.Series_multiplier)
        reps = round(reps * level.Reps_multiplier)

    return {
        "exercise": exercise,
        "series": series,
        "reps": reps,
    }


def build_routine_exercises(routine_exercises: list, user: User) -> list[dict]:
    return [apply_level_to_exercise(re, user) for re in routine_exercises]


# --- Casos de uso ---
def classify_user(user_id: int, area_id: int, level_id: int) -> User_Area_Level:
    user  = repo.get_user_by_id(user_id)
    area  = repo.get_area_by_id(area_id)
    level = repo.get_level_by_id(level_id)
    return repo.upsert_user_area_level(user, area, level)


def generate_training_plan(user_id: int, duration_days: int) -> Routine:
    user = repo.get_user_by_id(user_id)

    validate_user_goal(user)
    validate_user_levels(user)

    goal_routines      = repo.get_goal_routines(user)
    routine_exercises  = repo.get_exercises_from_routines(goal_routines)
    validate_available_exercises(routine_exercises, required=1)

    adjusted_exercises = build_routine_exercises(routine_exercises, user)

    routine = repo.create_routine(name=f"Rutina generada - {user.name}")
    repo.create_user_routine(user, routine, duration_days)
    repo.bulk_create_routine_exercises(routine, adjusted_exercises)

    return routine


def adjust_training_plan(user_id: int, routine_id: int, duration_days: int) -> Routine:
    user    = repo.get_user_by_id(user_id)
    routine = repo.get_routine_by_id(routine_id)

    validate_user_goal(user)
    validate_user_levels(user)

    repo.update_user_routine_time(user, routine, duration_days)
    repo.delete_routine_exercises(routine)
    generate_training_plan(user_id, duration_days)

    return routine