# ─────────────────────────────────────────────────────────────────────────────
# Repository  –  gym_app/repositories/user_repo.py
#
# Acceso a la base de datos para entidades del Usuario.
# Toda interacción con el ORM de Django ocurre aquí.
# No contiene lógica de negocio.
#
# Entidades: User, UserProfile, PhysicalTestResult,
#            TrainingPlan, TrainingSession, SessionExercise
# ─────────────────────────────────────────────────────────────────────────────

# from django.contrib.auth.models import User
from gym_app.models import User, User_Routine, Routine_Exercise, User_Area_Level


def save_user(email: str, password: str, username: str = None):
    return User.objects.create(
        username=username or email.split('@')[0],
        email=email,
        password=password
    )

def save_user_profile(user_id: int, age: int, weight: float, goal_id: int):
    user = User.objects.get(id=user_id)
    user.age = age
    user.weight = weight
    user.goal_id = goal_id
    user.save()
    return user

def save_physical_test(user_id: int, test_data: dict):
    # Aquí se guardaría el resultado del test físico en la base de datos
    # Por simplicidad, este ejemplo no implementa un modelo específico para los resultados del test
    print(f"Resultados del test físico para usuario ID {user_id}: {test_data}")

def fetch_latest_physical_test(user_id: int):
    # Aquí se recuperaría el resultado más reciente del test físico para el usuario
    # Por simplicidad, este ejemplo devuelve un resultado simulado
    return {"flexibilidad": 4, "fuerza": 8}

def fetch_user_by_email(email: str):
    return User.objects.filter(email=email).first()

def fetch_user_by_name(name: str):
    return User.objects.filter(name=name).first()

def fetch_user_by_username(username: str):
    return fetch_user_by_name(username)

def fetch_user_routines(user_id: int):
    routines = {}
    for ur in User_Routine.objects.filter(user=user_id).select_related('routine'):
        routines[ur.routine.name] = ur.routine.id
    return routines

def fetch_routine_exercises(routine_id: int):
    exercises = []
    for re in Routine_Exercise.objects.filter(routine=routine_id).select_related('exercise'):
        exercises.append({
            "name": re.exercise.name,
            "description": re.exercise.description,
            "series": re.series,
            "reps": re.reps,
            "load": re.load
        })
    return exercises

def fetch_user_profile(user_id: int):
    profile =User.objects.select_related('goal').get(id=user_id)
    return {
        "name": profile.name,
        "email": profile.email,
        "age": profile.age,
        "weight": profile.weight,
        "goal": profile.goal.name
    }