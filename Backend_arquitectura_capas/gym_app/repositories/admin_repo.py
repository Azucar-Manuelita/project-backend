# ─────────────────────────────────────────────────────────────────────────────
# Repository  –  gym_app/repositories/admin_repo.py
#
# Acceso a la base de datos para entidades administradas por el Admin.
# Toda interacción con el ORM de Django ocurre aquí.
# No contiene lógica de negocio.
#
# Entidades: Machine, Exercise, TrainingPlan, TrainingSession, SessionExercise
# ─────────────────────────────────────────────────────────────────────────────

from gym_app.models import Machine, Exercise, Area
def create_machine(name, area, image=None):
    return Machine.objects.create(
        name=name,
        area=Area.objects.get(name=area),
        image=image
    )

def fetch_machine_by_name(name: str):
    return Machine.objects.filter(name=name).first()


def fetch_machine_by_id(machine_id: int):
    return Machine.objects.filter(id=machine_id).first()


def fetch_all_machines():
    return Machine.objects.all()


def create_exercise(name: str, area: str, description: str):
    return Exercise.objects.create(
        name=name,
        area=Area.objects.get(name=area),
        description=description
    )

def fetch_exercises_by_machine(machine_id: int):
    return Exercise.objects.filter(area = Machine.objects.get(id=machine_id).area)
