# ─────────────────────────────────────────────────────────────────────────────
# Controllers  –  gym_app/controllers/validation_controller.py
#
# Punto de entrada HTTP para operaciones de validación y ajuste de planes.
# Recibe la petición, valida la estructura del request y delega
# al Validation Service. No contiene lógica de negocio.
#
# Casos de uso cubiertos:
#   RF_4  – Clasificar usuario según resultados y objetivos  (CU_04)
#   RF_5  – Generar plan de entrenamiento personalizado      (CU_05)
#   RF_11 – Ajustar plan según progreso y perfil             (CU_11)
# ─────────────────────────────────────────────────────────────────────────────

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
# from gym_app.services.validation_services import (
#     classify_user, adjust_training_plan,
# )


@require_http_methods(["POST"])
def classify_user(request, user_id: int):
    """
    RF_4 (CU_04) – Clasificar al usuario según sus resultados de prueba
    física y objetivos declarados.

    Método : POST  /training/<user_id>/classify/
    Retorna: 200 nivel asignado | 400 datos insuficientes | 404 usuario no existe
    """
    pass


@require_http_methods(["POST"])
def adjust_plan(request, user_id: int):
    """
    RF_11 (CU_11) – Ajustar el plan de entrenamiento activo ante cambios
    en el perfil o nuevos datos de progreso del usuario.

    Método : POST  /training/<user_id>/adjust/
    Retorna: 200 plan ajustado con comparación | 404 usuario o plan no existe
    """
    pass
