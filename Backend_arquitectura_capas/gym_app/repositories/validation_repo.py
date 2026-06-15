from gym_app.models import (
    User, Goal_Routine, Routine, Routine_Exercise,
    Exercise, Level, User_Area_Level, User_Routine, Area
)


# --- User ---
def get_user_by_id(user_id: int) -> User:
    return User.objects.get(id=user_id)

def fetch_goal(goal_id: int):
    from gym_app.models import Goal
    return Goal.objects.filter(id=goal_id).first()

# --- Area / Level ---
def get_area_by_id(area_id: int) -> Area:
    return Area.objects.get(id=area_id)


def get_level_by_id(level_id: int) -> Level:
    return Level.objects.get(id=level_id)


def get_user_level_for_area(user: User, area: Area) -> Level | None:
    entry = User_Area_Level.objects.filter(User_id=user, Area_id=area).first()
    return entry.Level_id if entry else None


def user_has_area_levels(user: User) -> bool:
    return User_Area_Level.objects.filter(User_id=user).exists()


def upsert_user_area_level(user: User, area: Area, level: Level) -> User_Area_Level:
    entry, _ = User_Area_Level.objects.update_or_create(
        User_id=user,
        Area_id=area,
        defaults={"Level_id": level},
    )
    return entry


# --- Routines ---
def get_routine_by_id(routine_id: int) -> Routine:
    return Routine.objects.get(id=routine_id)


def get_goal_routines(user: User) -> list:
    return list(
        Goal_Routine.objects.filter(Goal_id=user.goal_id)
        .select_related('routine_id')
    )


def user_owns_routine(user: User, routine: Routine) -> bool:
    return User_Routine.objects.filter(User_id=user, Routine_id=routine).exists()


def create_routine(name: str) -> Routine:
    return Routine.objects.create(name=name)


def create_user_routine(user: User, routine: Routine, duration_days: int) -> User_Routine:
    return User_Routine.objects.create(
        User_id=user,
        Routine_id=routine,
        Time=duration_days,
    )


def update_user_routine_time(user: User, routine: Routine, duration_days: int):
    User_Routine.objects.filter(User_id=user, Routine_id=routine).update(Time=duration_days)


# --- Exercises ---
def get_exercises_from_routines(goal_routines: list) -> list:
    routine_ids = [gr.Routine_id for gr in goal_routines]
    return list(
        Routine_Exercise.objects.filter(Routine_id__in=routine_ids)
        .select_related('Exercise_id', 'Exercise_id__MuscularArea_id')
    )


def bulk_create_routine_exercises(routine: Routine, exercises: list[dict]):
    Routine_Exercise.objects.bulk_create([
        Routine_Exercise(
            Routine_id=routine,
            Exercise_id=ex["exercise"],
            Series=ex["series"],
            Reps=ex["reps"],
        )
        for ex in exercises
    ])


def delete_routine_exercises(routine: Routine):
    Routine_Exercise.objects.filter(Routine_id=routine).delete()