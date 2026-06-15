# ─────────────────────────────────────────────────────────────────────────────
# Controllers  –  gym_app/controllers/user_controller.py
#
# Punto de entrada HTTP para operaciones del Usuario.
# Recibe la petición, valida la estructura del request y delega
# al User Service. No contiene lógica de negocio.
#
# Casos de uso cubiertos:
#   RF_2  – Registrar nuevo usuario              (CU_02)
#   RF_3  – Registrar datos iniciales            (CU_03)
#   RF_6  – Visualizar plan por sesiones         (CU_06)
#   RF_7  – Actualizar datos de usuario          (CU_07)
#   RF_8  – Visualizar detalles de ejercicio     (CU_08)
#   RF_9  – Visualizar información personal      (CU_09)
#   RF_10 – Iniciar sesión                       (CU_10)
# ─────────────────────────────────────────────────────────────────────────────

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
# from gym_app.services.user_services import (
#     register_user, authenticate_user,
#     register_initial_data, update_user_data, get_user_info,
#     get_training_plan_by_sessions, get_session_details,
#     get_exercise_details_in_session,
# )


@require_http_methods(["POST"])
def register_user(request):
    """
    RF_2 (CU_02) – Registrar un nuevo usuario en el sistema.

    Método : POST  /users/register/
    Body   : { "email": str, "password": str,
               "confirm_password": str, "username": str (opcional) }
    Retorna: 200 usuario creado | 400 datos inválidos | 409 correo ya existe
    """
    pass


@require_http_methods(["POST"])
def login(request):
    """
    RF_10 (CU_10) – Iniciar sesión con credenciales del usuario.

    Método : POST  /users/login/
    Body   : { "email_or_username": str, "password": str }
    Retorna: 200 sesión iniciada | 401 credenciales incorrectas | 404 usuario no existe
    """
    pass


@require_http_methods(["POST"])
def register_initial_data(request, user_id: int):
    """
    RF_3 (CU_03) – Registrar los datos físicos iniciales del usuario.

    Método : POST  /users/<user_id>/initial-data/
    Body   : { "age": int, "weight": float, "height": float,
               "goal_id": int, "training_period": int,
               "weekly_frequency": int,
               "physical_test_data": { "resistance_level": int,
                                       "strength_level": int,
                                       "flexibility_level": int },
               "limitation_ids": [int] (opcional) }
    Retorna: 200 datos registrados | 400 campos faltantes | 404 usuario no existe
    """
    pass


@require_http_methods(["PUT"])
def update_user_data(request, user_id: int):
    """
    RF_7 (CU_07) – Actualizar datos físicos u objetivos del usuario.

    Método : PUT   /users/<user_id>/update/
    Body   : mismos campos opcionales que RF_3
    Retorna: 200 perfil actualizado | 400 datos inválidos | 404 usuario no existe
    """
    pass


@require_http_methods(["GET"])
def get_user_info(request, user_id: int):
    """
    RF_9 (CU_09) – Obtener la información personal completa del usuario.

    Método : GET  /users/<user_id>/info/
    Retorna: 200 información personal | 404 usuario no existe
    """
    pass


@require_http_methods(["GET"])
def get_plan_sessions(request, user_id: int):
    """
    RF_6 (CU_06) – Obtener el plan activo organizado por sesiones/días.

    Método : GET  /training/<user_id>/plan/
    Retorna: 200 plan con sesiones | 404 usuario o plan no existe
    """
    pass


@require_http_methods(["GET"])
def get_session_details(request, session_id: int):
    """
    RF_6 (CU_06) – Obtener los detalles de una sesión con su lista de ejercicios.

    Método : GET  /training/sessions/<session_id>/
    Retorna: 200 detalles de la sesión | 404 sesión no existe
    """
    pass


@require_http_methods(["GET"])
def get_exercise_details(request, session_id: int, exercise_id: int):
    """
    RF_8 (CU_08) – Obtener la información detallada de un ejercicio en una sesión.

    Método : GET  /training/sessions/<session_id>/exercises/<exercise_id>/
    Retorna: 200 detalles del ejercicio | 404 no encontrado
    """
    pass
