from gym_app.repositories import admin_repo

def no_invalid_chars(name: str)-> bool:
    invalid_chars = set('!@#$%^&*()+=[]{}|\\;:"<>,.?/')
    if len(invalid_chars.intersection(name)) != 0:
        return False
    return True
def valid_name_length(name: str) -> bool:
    return 1 <= len(name) <= 50

def register_machine(name: str, area: str):
    if not no_invalid_chars(name):
        raise ValueError("El nombre de la máquina contiene caracteres no permitidos.")

    if not valid_name_length(name):
        raise ValueError("El nombre de la máquina debe tener entre 1 y 50 caracteres.") 

    if area not in ['ARMS', 'CHEST', 'BACK', 'ABDOMEN', 'LEGS', 'CARDIO']:
        raise ValueError("Área corporal no elegida.")
    if admin_repo.machine_name_exists(name):
        raise ValueError("Ya existe una máquina con ese nombre.")  
    name = name.upper()
    admin_repo.create_machine(
        name=name,
        area=area
    )
    return True
    

def correct_description_length(description: str) -> bool:
    return len(description) <= 500

def register_exercise(name: str, description: str, area: str):
    if not no_invalid_chars(name):
        raise ValueError("El nombre del ejercicio contiene caracteres no permitidos.")  
    if not valid_name_length(name):
        raise ValueError("El nombre del ejercicio debe tener entre 1 y 50 caracteres.")
    if area not in ['ARMS', 'CHEST', 'BACK', 'ABDOMEN', 'LEGS', 'CARDIO']:
        raise ValueError("Área corporal no elegida.")
    if not correct_description_length(description):
        raise ValueError("La descripción del ejercicio no puede exceder los 500 caracteres.")
    name = name.upper()
    if admin_repo.exercise_name_exists(name):
        raise ValueError("Ya existe un ejercicio con ese nombre.")
    admin_repo.create_exercise(
        name=name,
        description=description,
        MuscularArea=area
    )
    return "Ejercicio registrado exitosamente."



def get_all_machines():
    """
    Obtener la lista completa de máquinas registradas.

    Retorna:
        QuerySet[Machine]
    """
    pass


def get_machine_by_id(machine_id: int):
    """
    Obtener una máquina por su ID.

    Parámetros:
        machine_id (int) – ID de la máquina.

    Retorna:
        Machine

    Lanza:
        Machine.DoesNotExist – si no existe.
    """
    pass


def get_exercises_by_machine(machine_id: int):
    """
    Obtener todos los ejercicios de una máquina específica.

    Parámetros:
        machine_id (int) – ID de la máquina.

    Retorna:
        QuerySet[Exercise]

    Lanza:
        Machine.DoesNotExist – si no existe.
    """
    pass


def generate_training_plan(user_id: int):
    """
    RF_5 (CU_05) – Generar un plan de entrenamiento personalizado a partir
    del perfil clasificado del usuario, seleccionando ejercicios disponibles
    y organizándolos en sesiones según la frecuencia semanal declarada.

    Parámetros:
        user_id (int) – ID del usuario.

    Retorna:
        TrainingPlan – plan generado y marcado como activo.

    Lanza:
        UserProfile.DoesNotExist – perfil no existe.
        ValueError               – el usuario no tiene clasificación o no hay
                                   ejercicios suficientes en la BD.
    """
    pass
