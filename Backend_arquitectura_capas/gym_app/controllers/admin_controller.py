# ─────────────────────────────────────────────────────────────────────────────
# Controllers  –  gym_app/controllers/admin_controller.py
#
# Punto de entrada HTTP para operaciones del Administrador.
# Recibe la petición, valida la estructura del request y delega
# al Admin Service. No contiene lógica de negocio.
#
# Casos de uso cubiertos:
#   RF_1  – Registrar máquinas (CU_01a) y ejercicios (CU_01b)
#   RF_5  – Generar plan de entrenamiento personalizado (CU_05)
# ─────────────────────────────────────────────────────────────────────────────

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
# from gym_app.services.admin_services import (
#     register_machine, register_exercise,
#     get_all_machines, get_machine_exercises,
#     generate_training_plan,
# )


@require_http_methods(["POST"])
def add_machine(request):
    """
    RF_1 (CU_01a) – Registrar una nueva máquina en el gimnasio.

    Método : POST  /machines/add/
    Body   : { "name": str, "image": file (opcional) }
    Retorna: 200 máquina creada | 400 datos inválidos | 409 ya existe
    """
    pass


@require_http_methods(["POST"])
def add_exercise(request, machine_id: int):
    """
    RF_1 (CU_01b) – Registrar un ejercicio asociado a una máquina.

    Método : POST  /machines/<machine_id>/exercises/add/
    Body   : { "name": str, "body_area": str,
               "description": str, "image": file (opcional) }
    Retorna: 200 ejercicio creado | 400 datos inválidos | 404 máquina no existe | 409 ya existe
    """
    pass


@require_http_methods(["GET"])
def get_machines(request):
    """
    Listar todas las máquinas registradas.

    Método : GET  /machines/
    Retorna: 200 lista de máquinas
    """
    pass


@require_http_methods(["GET"])
def get_machine_exercises(request, machine_id: int):
    """
    Listar todos los ejercicios de una máquina.

    Método : GET  /machines/<machine_id>/exercises/
    Retorna: 200 lista de ejercicios | 404 máquina no existe
    """
    pass


@require_http_methods(["POST"])
def generate_plan(request, user_id: int):
    """
    RF_5 (CU_05) – Generar el plan de entrenamiento personalizado de un usuario.

    Método : POST  /training/<user_id>/generate/
    Retorna: 200 plan generado | 400 perfil incompleto | 404 usuario no existe
    """
    pass
