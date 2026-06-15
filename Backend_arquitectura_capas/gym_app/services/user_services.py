# ─────────────────────────────────────────────────────────────────────────────
# Services  –  gym_app/services/user_services.py
#
# Lógica de negocio para operaciones del Usuario.
# Orquesta las reglas del dominio y delega la persistencia al User Repository.
#
# Casos de uso cubiertos:
#   RF_2  – Registrar nuevo usuario          (CU_02)
#   RF_3  – Registrar datos iniciales        (CU_03)
#   RF_6  – Visualizar plan por sesiones     (CU_06)
#   RF_7  – Actualizar datos de usuario      (CU_07)
#   RF_8  – Visualizar detalles de ejercicio (CU_08)
#   RF_9  – Visualizar información personal  (CU_09)
#   RF_10 – Iniciar sesión                   (CU_10)
# ─────────────────────────────────────────────────────────────────────────────

from typing import List, Dict, Any
from gym_app.repositories import user_repo, validation_repo
import re
import hashlib
import gym_app.tests.ranges_physic_test as ranges


def save_user(email: str, password: str):
    return user_repo.save_user(email, password)


def save_user_profile(user_id: int, age: int, weight: float, goal_id: int):
    return user_repo.save_user_profile(user_id, age, weight, goal_id)


def save_physical_test(user_id: int, test_data: dict):
    return user_repo.save_physical_test(user_id, test_data)


def fetch_latest_physical_test(user_id: int):
    return user_repo.fetch_latest_physical_test(user_id)


def fetch_user_profile(user_id: int):
    return user_repo.fetch_user_profile(user_id)


def fetch_user_by_email(email: str):
    return user_repo.fetch_user_by_email(email)


def fetch_goal(goal_id: int):
    return validation_repo.fetch_goal(goal_id)

def empty(email: str, password: str, confirm_password: str):
    return not email or not password or not confirm_password

def valid_email(email):
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(patron, email) is not None

def valid_passord(password):
    if not valid_lenght(password):
        return False
    if not valid_uppercase(password):
        return False
    if not valid_lowercase(password):
        return False
    if not valid_digit(password):
        return False
    if not valid_special_char(password):
        return False
    return True


def valid_lenght(password):
    return len(password) >= 8


def valid_uppercase(password):
    return any(c.isupper() for c in password)


def valid_lowercase(password):
    return any(c.islower() for c in password)


def valid_digit(password):
    return any(c.isdigit() for c in password)


def valid_special_char(password):
    special_characters = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/"
    return any(c in special_characters for c in password)


def same_passwords(password, confirm_password):
    return password == confirm_password


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(email: str, password: str, confirm_password: str):
    if empty(email, password, confirm_password):
        raise ValueError("Todos los campos son obligatorios.")
    if not valid_email(email):
        raise ValueError("Correo electrónico no es válido.")
    if not valid_passord(password):
        raise ValueError("La contraseña no cumple con los requisitos de seguridad.")
    if not same_passwords(password, confirm_password):
        raise ValueError("Las contraseñas no coinciden.")
    save_user(email, hash_password(password))
    print(f"Usuario con correo {email} registrado con éxito.")


def authenticate_user(email_or_username: str, password: str):
    user = fetch_user_by_email(email_or_username)
    if not user:
        raise ValueError("Usuario no encontrado.")
    if user.password != hash_password(password):
        raise ValueError("Contraseña incorrecta.")
    print(f"Usuario {user.email} autenticado con éxito.")
    return user

def validate_age(age):
    return age<ranges.Realistic_ranges["age"]["min"] or age>ranges.Realistic_ranges["age"]["max"]

def validate_weight(weight):
    return weight<ranges.Realistic_ranges["weight"]["min"] or weight>ranges.Realistic_ranges["weight"]["max"]    

def register_initial_data(user_id: int, age: int, weight: float, goal_id: int, physical_test_data: dict,):
    if not fetch_goal(goal_id):
        raise ValueError("El objetivo de entrenamiento no es válido.")
    
    if validate_age(age):
        raise ValueError("La edad no cumple con el rango realista.")
    
    if validate_weight(weight):
        raise ValueError("El peso no cumple con el rango realista.")
    
    profile = save_user_profile(user_id, age, weight, goal_id)
    save_physical_test(profile.id, physical_test_data)
    print(f"Datos iniciales registrados para usuario ID {user_id}.")


def update_user_data(user_id: int, age: int = None, weight: float = None, goal_id: int = None, physical_test_data: dict = None,):
    original_profile = fetch_user_profile(user_id)
    original_test = fetch_latest_physical_test(user_id)

    new_age = age if age is not None else original_profile.age
    new_weight = weight if weight is not None else original_profile.weight
    new_goal_id = goal_id if goal_id is not None else original_profile.goal_id

    if physical_test_data is None:
        physical_test_data = original_test.results

    if not fetch_goal(new_goal_id):
        raise ValueError("El objetivo de entrenamiento no es válido.")

    if validate_age(new_age):
        raise ValueError("La edad no cumple con el rango realista.")

    if validate_weight(new_weight):
        raise ValueError("El peso no cumple con el rango realista.")

    profile = save_user_profile(user_id, new_age, new_weight, new_goal_id)
    save_physical_test(profile.id, physical_test_data)
    print(f"Datos actualizados registrados para usuario ID {user_id}.")



def get_user_routines_service(user_id: int) -> List[Dict[str, Any]]:
    """
    RF_6: Fetch all routines associated with a user.
    Returns routine names/IDs.
    """
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("Invalid user ID. It must be a positive integer.")
    
    routines = list(user_repo.fetch_user_routines(user_id))
    
    if not routines:
        return []
        
    return routines


def get_routine_exercises_service(routine_id: int) -> List[Dict[str, Any]]:
    """
    RF_8: Fetch exercises for a routine.
    Combines fields from Rutine_Exercise (Series, Reps) and Exercise (name, description).
    """
    if not isinstance(routine_id, int) or routine_id <= 0:
        raise ValueError("Invalid routine ID. It must be a positive integer.")
        
    exercises = user_repo.fetch_routine_exercises(routine_id)
    
    if not exercises:
        return []
        
    return exercises


def get_user_profile_service(user_id: int) -> Dict[str, Any]:
    """
    RF_9: Fetch personal information and current state of the user.
    Security Rule: Password must never be exposed.
    """
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("Invalid user ID. It must be a positive integer.")
        
    user_data = user_repo.fetch_user_profile(user_id)
    
    if not user_data:
        raise ValueError("User not found.")
        
    if "password" in user_data:
        del user_data["password"]
        
    return user_data