# ─────────────────────────────────────────────────────────────────────────────
# core/urls.py  –  Enrutamiento de la API
#
# Las URLs mapean directamente a los Controllers.
# Prefijos:
#   /machines/   – Admin: máquinas y ejercicios
#   /users/      – User: registro, sesión, perfil
#   /training/   – User / Validation: plan, sesiones, clasificación, ajuste
# ─────────────────────────────────────────────────────────────────────────────

from django.contrib import admin
from django.urls import path
from gym_app.views import prueba_conexion
from gym_app.controllers import admin_controller, user_controller, validation_controller

urlpatterns = [
    path('admin/', admin.site.urls),

    # ── Prueba de conexión (existente) ────────────────────────────────────
    path('test/', prueba_conexion),

    # ── RF_1: Máquinas y Ejercicios  (Admin Controller) ──────────────────
    path('machines/',                                admin_controller.get_machines,         name='get_machines'),
    path('machines/add/',                            admin_controller.add_machine,          name='add_machine'),
    path('machines/<int:machine_id>/exercises/',     admin_controller.get_machine_exercises,name='get_machine_exercises'),
    path('machines/<int:machine_id>/exercises/add/', admin_controller.add_exercise,         name='add_exercise'),

    # ── RF_2: Registro de usuario  (User Controller) ─────────────────────
    path('users/register/',                          user_controller.register_user,         name='register_user'),

    # ── RF_10: Inicio de sesión  (User Controller) ───────────────────────
    path('users/login/',                             user_controller.login,                 name='login'),

    # ── RF_3: Datos iniciales  (User Controller) ─────────────────────────
    path('users/<int:user_id>/initial-data/',        user_controller.register_initial_data, name='register_initial_data'),

    # ── RF_7: Actualizar datos  (User Controller) ────────────────────────
    path('users/<int:user_id>/update/',              user_controller.update_user_data,      name='update_user_data'),

    # ── RF_9: Información personal  (User Controller) ────────────────────
    path('users/<int:user_id>/info/',                user_controller.get_user_info,         name='get_user_info'),

    # ── RF_4: Clasificar usuario  (Validation Controller) ────────────────
    path('training/<int:user_id>/classify/',         validation_controller.classify_user,   name='classify_user'),

    # ── RF_5: Generar plan  (Admin Controller) ───────────────────────────
    path('training/<int:user_id>/generate/',         admin_controller.generate_plan,        name='generate_plan'),

    # ── RF_6: Plan por sesiones  (User Controller) ───────────────────────
    path('training/<int:user_id>/plan/',             user_controller.get_plan_sessions,     name='get_plan_sessions'),
    path('training/sessions/<int:session_id>/',      user_controller.get_session_details,   name='get_session_details'),

    # ── RF_8: Detalles de ejercicio  (User Controller) ───────────────────
    path('training/sessions/<int:session_id>/exercises/<int:exercise_id>/',
         user_controller.get_exercise_details, name='get_exercise_details'),

    # ── RF_11: Ajustar plan  (Validation Controller) ─────────────────────
    path('training/<int:user_id>/adjust/',           validation_controller.adjust_plan,     name='adjust_plan'),
]
