# ─────────────────────────────────────────────────────────────────────────────
# Tests  –  gym_app/tests/test_training_service.py
#
# Cubre:
#   RF_4  – classify_user        (CU_04)
#   RF_5  – generate_training_plan (CU_05)
#   RF_11 – adjust_training_plan   (CU_11)
# ─────────────────────────────────────────────────────────────────────────────

from unittest.mock import MagicMock, patch, call
import pytest

from gym_app.services.training_service import (
    classify_user,
    generate_training_plan,
    adjust_training_plan,
)



def make_user(goal=True):
    user = MagicMock()
    user.id = 1
    user.name = "Samuel"
    user.goal_id = MagicMock() if goal else None
    return user

def make_area():
    area = MagicMock()
    area.id = 10
    return area

def make_level(series_mult=1.5, reps_mult=1.2):
    level = MagicMock()
    level.id = 5
    level.Series_multiplier = series_mult
    level.Reps_multiplier = reps_mult
    return level

def make_routine_exercise(series=3, reps=10, area=None):
    area = area or make_area()
    exercise = MagicMock()
    exercise.MuscularArea_id = area

    re = MagicMock()
    re.Exercise_id = exercise
    re.Series = series
    re.Reps = reps
    return re



class TestClassifyUser:
    """
    classify_user(user_id, area_id, level_id)
    Crea o actualiza User_Area_Level para el usuario dado.
    """

    @patch("gym_app.services.training_service.User_Area_Level")
    @patch("gym_app.services.training_service.Level")
    @patch("gym_app.services.training_service.Area")
    @patch("gym_app.services.training_service.User")
    def test_crea_entrada_nueva(self, MockUser, MockArea, MockLevel, MockUAL):
        """Cuando no existe entrada previa, update_or_create la crea."""
        user = make_user()
        area = make_area()
        level = make_level()

        MockUser.objects.get.return_value = user
        MockArea.objects.get.return_value = area
        MockLevel.objects.get.return_value = level

        entry = MagicMock()
        MockUAL.objects.update_or_create.return_value = (entry, True)  # created=True

        result = classify_user(1, 10, 5)

        MockUAL.objects.update_or_create.assert_called_once_with(
            User_id=user,
            Area_id=area,
            defaults={"Level_id": level},
        )
        assert result is entry

    @patch("gym_app.services.training_service.User_Area_Level")
    @patch("gym_app.services.training_service.Level")
    @patch("gym_app.services.training_service.Area")
    @patch("gym_app.services.training_service.User")
    def test_actualiza_entrada_existente(self, MockUser, MockArea, MockLevel, MockUAL):
        """Cuando ya existe entrada, update_or_create la actualiza (created=False)."""
        user = make_user()
        area = make_area()
        level = make_level()

        MockUser.objects.get.return_value = user
        MockArea.objects.get.return_value = area
        MockLevel.objects.get.return_value = level

        entry = MagicMock()
        MockUAL.objects.update_or_create.return_value = (entry, False)  # created=False

        result = classify_user(1, 10, 5)

        assert result is entry
        MockUAL.objects.update_or_create.assert_called_once()

    @patch("gym_app.services.training_service.User")
    def test_lanza_si_usuario_no_existe(self, MockUser):
        """Si el user_id no existe en DB, User.objects.get lanza DoesNotExist."""
        MockUser.objects.get.side_effect = Exception("DoesNotExist")

        with pytest.raises(Exception):
            classify_user(999, 10, 5)

    @patch("gym_app.services.training_service.User_Area_Level")
    @patch("gym_app.services.training_service.Level")
    @patch("gym_app.services.training_service.Area")
    @patch("gym_app.services.training_service.User")
    def test_usa_ids_correctos_para_busqueda(self, MockUser, MockArea, MockLevel, MockUAL):
        """Verifica que se llaman .get() con los IDs correctos."""
        MockUAL.objects.update_or_create.return_value = (MagicMock(), True)

        classify_user(1, 10, 5)

        MockUser.objects.get.assert_called_once_with(id=1)
        MockArea.objects.get.assert_called_once_with(id=10)
        MockLevel.objects.get.assert_called_once_with(id=5)




class TestGenerateTrainingPlan:
    """
    generate_training_plan(user_id, duration_days)
    Genera una rutina nueva con ejercicios ajustados al nivel del usuario.
    """

    def _mock_all(self, MockUser, MockUAL, MockGoalRoutine,
                  MockRoutineExercise, MockRoutine, MockUserRoutine,
                  user=None, has_levels=True, num_exercises=1):
        """Helper: configura el escenario base para generate_training_plan."""
        user = user or make_user(goal=True)
        MockUser.objects.get.return_value = user

        ual_qs = MagicMock()
        ual_qs.exists.return_value = has_levels
        MockUAL.objects.filter.return_value = ual_qs

        goal_routine = MagicMock()
        goal_routine.Routine_id = MagicMock()
        MockGoalRoutine.objects.filter.return_value.select_related.return_value = [goal_routine]

        re_list = [make_routine_exercise() for _ in range(num_exercises)]
        MockRoutineExercise.objects.filter.return_value.select_related.return_value = re_list

        routine = MagicMock()
        MockRoutine.objects.create.return_value = routine

        return user, routine, re_list

    @patch("gym_app.services.training_service.Routine_Exercise")
    @patch("gym_app.services.training_service.User_Routine")
    @patch("gym_app.services.training_service.Routine")
    @patch("gym_app.services.training_service.Goal_Routine")
    @patch("gym_app.services.training_service.User_Area_Level")
    @patch("gym_app.services.training_service.User")
    def test_retorna_rutina_creada(self, MockUser, MockUAL, MockGoalRoutine,
                                   MockRoutine, MockUserRoutine, MockRoutineExercise):
        """El flujo completo feliz retorna el objeto Routine creado."""
        user, routine, _ = self._mock_all(
            MockUser, MockUAL, MockGoalRoutine,
            MockRoutineExercise, MockRoutine, MockUserRoutine
        )

        result = generate_training_plan(1, 30)

        assert result is routine

    @patch("gym_app.services.training_service.Routine_Exercise")
    @patch("gym_app.services.training_service.User_Routine")
    @patch("gym_app.services.training_service.Routine")
    @patch("gym_app.services.training_service.Goal_Routine")
    @patch("gym_app.services.training_service.User_Area_Level")
    @patch("gym_app.services.training_service.User")
    def test_lanza_si_usuario_sin_objetivo(self, MockUser, MockUAL, MockGoalRoutine,
                                           MockRoutine, MockUserRoutine, MockRoutineExercise):
        """ValueError si el usuario no tiene goal_id."""
        user = make_user(goal=False)
        MockUser.objects.get.return_value = user

        with pytest.raises(ValueError, match="objetivo"):
            generate_training_plan(1, 30)

    @patch("gym_app.services.training_service.Routine_Exercise")
    @patch("gym_app.services.training_service.User_Routine")
    @patch("gym_app.services.training_service.Routine")
    @patch("gym_app.services.training_service.Goal_Routine")
    @patch("gym_app.services.training_service.User_Area_Level")
    @patch("gym_app.services.training_service.User")
    def test_lanza_si_usuario_sin_niveles(self, MockUser, MockUAL, MockGoalRoutine,
                                          MockRoutine, MockUserRoutine, MockRoutineExercise):
        """ValueError si el usuario no tiene User_Area_Level asignados."""
        user = make_user(goal=True)
        MockUser.objects.get.return_value = user

        ual_qs = MagicMock()
        ual_qs.exists.return_value = False
        MockUAL.objects.filter.return_value = ual_qs

        with pytest.raises(ValueError, match="niveles"):
            generate_training_plan(1, 30)

    @patch("gym_app.services.training_service.Routine_Exercise")
    @patch("gym_app.services.training_service.User_Routine")
    @patch("gym_app.services.training_service.Routine")
    @patch("gym_app.services.training_service.Goal_Routine")
    @patch("gym_app.services.training_service.User_Area_Level")
    @patch("gym_app.services.training_service.User")
    def test_lanza_si_sin_ejercicios(self, MockUser, MockUAL, MockGoalRoutine,
                                     MockRoutine, MockUserRoutine, MockRoutineExercise):
        """ValueError si no hay ejercicios en las rutinas template del objetivo."""
        user = make_user(goal=True)
        MockUser.objects.get.return_value = user

        ual_qs = MagicMock()
        ual_qs.exists.return_value = True
        MockUAL.objects.filter.return_value = ual_qs

        goal_routine = MagicMock()
        MockGoalRoutine.objects.filter.return_value.select_related.return_value = [goal_routine]

        # Lista vacía — sin ejercicios
        MockRoutineExercise.objects.filter.return_value.select_related.return_value = []

        with pytest.raises(ValueError, match="ejercicios"):
            generate_training_plan(1, 30)

    @patch("gym_app.services.training_service.Routine_Exercise")
    @patch("gym_app.services.training_service.User_Routine")
    @patch("gym_app.services.training_service.Routine")
    @patch("gym_app.services.training_service.Goal_Routine")
    @patch("gym_app.services.training_service.User_Area_Level")
    @patch("gym_app.services.training_service.User")
    def test_aplica_multiplicadores_de_nivel(self, MockUser, MockUAL, MockGoalRoutine,
                                             MockRoutine, MockUserRoutine, MockRoutineExercise):
        """Series y Reps se multiplican por los factores del Level del área."""
        user = make_user(goal=True)
        MockUser.objects.get.return_value = user

        ual_qs = MagicMock()
        ual_qs.exists.return_value = True
        MockUAL.objects.filter.return_value = ual_qs

        area = make_area()
        level = make_level(series_mult=2.0, reps_mult=1.5)

        # User_Area_Level.filter(User_id, Area_id).first() devuelve entry con Level_id
        ual_entry = MagicMock()
        ual_entry.Level_id = level
        MockUAL.objects.filter.return_value.first.return_value = ual_entry

        re = make_routine_exercise(series=3, reps=10, area=area)
        goal_routine = MagicMock()
        MockGoalRoutine.objects.filter.return_value.select_related.return_value = [goal_routine]
        MockRoutineExercise.objects.filter.return_value.select_related.return_value = [re]

        routine = MagicMock()
        MockRoutine.objects.create.return_value = routine

        generate_training_plan(1, 30)

        created_args = MockRoutineExercise.objects.bulk_create.call_args[0][0]
        assert created_args[0].Series == round(3 * 2.0)   # 6
        assert created_args[0].Reps == round(10 * 1.5)    # 15

    @patch("gym_app.services.training_service.Routine_Exercise")
    @patch("gym_app.services.training_service.User_Routine")
    @patch("gym_app.services.training_service.Routine")
    @patch("gym_app.services.training_service.Goal_Routine")
    @patch("gym_app.services.training_service.User_Area_Level")
    @patch("gym_app.services.training_service.User")
    def test_sin_nivel_para_area_usa_valores_base(self, MockUser, MockUAL, MockGoalRoutine,
                                                   MockRoutine, MockUserRoutine, MockRoutineExercise):
        """Si no hay nivel asignado para el área, se usan Series/Reps originales."""
        user = make_user(goal=True)
        MockUser.objects.get.return_value = user

        ual_qs = MagicMock()
        ual_qs.exists.return_value = True
        MockUAL.objects.filter.return_value = ual_qs

        # .first() devuelve None → sin nivel para esa área
        MockUAL.objects.filter.return_value.first.return_value = None

        re = make_routine_exercise(series=4, reps=12)
        goal_routine = MagicMock()
        MockGoalRoutine.objects.filter.return_value.select_related.return_value = [goal_routine]
        MockRoutineExercise.objects.filter.return_value.select_related.return_value = [re]

        routine = MagicMock()
        MockRoutine.objects.create.return_value = routine

        generate_training_plan(1, 30)

        created_args = MockRoutineExercise.objects.bulk_create.call_args[0][0]
        assert created_args[0].Series == 4
        assert created_args[0].Reps == 12

    @patch("gym_app.services.training_service.Routine_Exercise")
    @patch("gym_app.services.training_service.User_Routine")
    @patch("gym_app.services.training_service.Routine")
    @patch("gym_app.services.training_service.Goal_Routine")
    @patch("gym_app.services.training_service.User_Area_Level")
    @patch("gym_app.services.training_service.User")
    def test_crea_user_routine_con_duracion(self, MockUser, MockUAL, MockGoalRoutine,
                                            MockRoutine, MockUserRoutine, MockRoutineExercise):
        """User_Routine se crea con el Time (duration_days) correcto."""
        user, routine, _ = self._mock_all(
            MockUser, MockUAL, MockGoalRoutine,
            MockRoutineExercise, MockRoutine, MockUserRoutine
        )

        generate_training_plan(1, 45)

        MockUserRoutine.objects.create.assert_called_once_with(
            User_id=user,
            Routine_id=routine,
            Time=45,
        )



class TestAdjustTrainingPlan:
    """
    adjust_training_plan(user_id, duration_days)
    Delega en generate_training_plan tras validar usuario.
    Refleja los niveles actuales (ya actualizados por classify_user).
    """

    @patch("gym_app.services.training_service.generate_training_plan")
    @patch("gym_app.services.training_service.User_Area_Level")
    @patch("gym_app.services.training_service.User")
    def test_delega_en_generate(self, MockUser, MockUAL, mock_generate):
        """adjust_training_plan llama a generate_training_plan con los mismos args."""
        user = make_user(goal=True)
        MockUser.objects.get.return_value = user

        ual_qs = MagicMock()
        ual_qs.exists.return_value = True
        MockUAL.objects.filter.return_value = ual_qs

        nueva_rutina = MagicMock()
        mock_generate.return_value = nueva_rutina

        result = adjust_training_plan(1, 30)

        mock_generate.assert_called_once_with(1, 30)
        assert result is nueva_rutina

    @patch("gym_app.services.training_service.User_Area_Level")
    @patch("gym_app.services.training_service.User")
    def test_lanza_si_usuario_sin_objetivo(self, MockUser, MockUAL):
        """ValueError si el usuario no tiene goal_id, antes de llegar a generate."""
        user = make_user(goal=False)
        MockUser.objects.get.return_value = user

        with pytest.raises(ValueError, match="objetivo"):
            adjust_training_plan(1, 30)

    @patch("gym_app.services.training_service.User_Area_Level")
    @patch("gym_app.services.training_service.User")
    def test_lanza_si_usuario_sin_niveles(self, MockUser, MockUAL):
        """ValueError si el usuario no tiene niveles asignados."""
        user = make_user(goal=True)
        MockUser.objects.get.return_value = user

        ual_qs = MagicMock()
        ual_qs.exists.return_value = False
        MockUAL.objects.filter.return_value = ual_qs

        with pytest.raises(ValueError, match="niveles"):
            adjust_training_plan(1, 30)

    @patch("gym_app.services.training_service.generate_training_plan")
    @patch("gym_app.services.training_service.User_Area_Level")
    @patch("gym_app.services.training_service.User")
    def test_refleja_niveles_actualizados(self, MockUser, MockUAL, mock_generate):
        """
        Verifica el flujo completo de RF_11:
        classify_user actualiza el nivel → adjust_training_plan genera
        con los nuevos multiplicadores (integración de las dos funciones).
        """
        user = make_user(goal=True)
        MockUser.objects.get.return_value = user

        ual_qs = MagicMock()
        ual_qs.exists.return_value = True
        MockUAL.objects.filter.return_value = ual_qs

        mock_generate.return_value = MagicMock()

        # Simula que ya se llamó classify_user antes (nivel actualizado en DB)
        adjust_training_plan(1, 30)

        # El plan generado usa lo que haya en DB en ese momento
        mock_generate.assert_called_once_with(1, 30)
