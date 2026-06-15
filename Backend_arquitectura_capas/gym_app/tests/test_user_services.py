import sys
import unittest
from unittest.mock import patch, MagicMock
sys.modules['django'] = MagicMock()
sys.modules['django.db'] = MagicMock()
sys.modules['django.contrib.auth.models'] = MagicMock()
import gym_app.services.user_services as user_services
import gym_app.tests.ranges_physic_test as ranges
from unittest import mock


class TestUserServices(unittest.TestCase):

    # ─────────────────────────────────────────────────────────────────────────
    # 1. PRUEBAS DE VALIDACIÓN DE CONTRASEÑAS Y EMAIL
    # ─────────────────────────────────────────────────────────────────────────

    def test_empty_fields(self):
        """Evalúa combinaciones de campos vacíos en el registro."""
        self.assertTrue(user_services.empty("", "Pass123!", "Pass123!"))
        self.assertTrue(user_services.empty("test@test.com", "", "Pass123!"))
        self.assertTrue(user_services.empty("test@test.com", "Pass123!", ""))
        self.assertFalse(user_services.empty("test@test.com", "Pass123!", "Pass123!"))

    def test_valid_email_boundaries(self):
        """Evalúa estructuras límites de correos electrónicos."""
        self.assertTrue(user_services.valid_email("a@b.co"))  # El caso más corto válido
        self.assertTrue(user_services.valid_email("user.name+regex@domain.com.co"))
        self.assertFalse(user_services.valid_email("usuario@dominio"))  # Sin TLD
        self.assertFalse(user_services.valid_email("@dominio.com"))  # Sin parte local
        self.assertFalse(user_services.valid_email("usuario.com"))  # Sin arroba

    def test_password_security_rules(self):
        """Prueba de forma exhaustiva las reglas complejas de la contraseña."""
        # Caso límite: Exactamente 8 caracteres con todos los requisitos (Válido)
        self.assertTrue(user_services.valid_passord("Ab1!aaaa"))
        
        # Caso límite: 7 caracteres (Inválido por longitud)
        self.assertFalse(user_services.valid_passord("Ab1!aaa"))
        
        # Faltan componentes críticos
        self.assertFalse(user_services.valid_passord("abcdef1!"))  # Sin Mayúscula
        self.assertFalse(user_services.valid_passord("ABCDEF1!"))  # Sin Minúscula
        self.assertFalse(user_services.valid_passord("Abcdefgh!")) # Sin Dígito
        self.assertFalse(user_services.valid_passord("Abcdefg1"))  # Sin Carácter Especial

    # ─────────────────────────────────────────────────────────────────────────
    # 2. PRUEBAS DE LÍMITES BIOMÉTRICOS Y RANGOS REALISTAS
    # ─────────────────────────────────────────────────────────────────────────
    # NOTA: Estas pruebas asumen la corrección lógica de 'and' a 'or' en el software.

    def test_validate_age_boundaries(self):
        """Prueba límites exactos para la edad (12 a 100)."""
        min_age = ranges.Realistic_ranges["age"]["min"]
        max_age = ranges.Realistic_ranges["age"]["max"]

        # Valores Frontera Válidos
        self.assertFalse(user_services.validate_age(min_age))      # 12 no debe levantar alarma (False)
        self.assertFalse(user_services.validate_age(max_age))      # 100 no debe levantar alarma (False)
        self.assertFalse(user_services.validate_age(35))           # Promedio válido

        # Valores Frontera Inválidos
        self.assertTrue(user_services.validate_age(min_age - 1))   # 11 es inválido (True)
        self.assertTrue(user_services.validate_age(max_age + 1))   # 101 es inválido (True)
        self.assertTrue(user_services.validate_age(-5))            # Negativo extremo

    def test_validate_weight_boundaries(self):
        """Prueba límites exactos para el peso (30 a 250)."""
        min_w = ranges.Realistic_ranges["weight"]["min"]
        max_w = ranges.Realistic_ranges["weight"]["max"]

        self.assertFalse(user_services.validate_weight(min_w))      # 30 Válido
        self.assertFalse(user_services.validate_weight(max_w))      # 250 Válido
        
        self.assertTrue(user_services.validate_weight(min_w - 0.1)) # 29.9 Inválido
        self.assertTrue(user_services.validate_weight(max_w + 0.1)) # 250.1 Inválido

    def test_validate_age_invalid_returns_true(self):
        """Verifica que una edad fuera de rango devuelva True."""
        self.assertTrue(user_services.validate_age(5))
        self.assertTrue(user_services.validate_age(101))

    def test_validate_weight_invalid_returns_true(self):
        """Verifica que un peso fuera de rango devuelva True."""
        self.assertTrue(user_services.validate_weight(10.0))
        self.assertTrue(user_services.validate_weight(300.0))

    # ─────────────────────────────────────────────────────────────────────────
    # 3. PRUEBAS DE MOCKING PARA CASOS DE USO (REPOSITORIOS)
    # ─────────────────────────────────────────────────────────────────────────

    @patch('gym_app.repositories.user_repo.save_user')
    def test_register_user_success(self, mock_save_user):
        """Verifica registro correcto y hasheo de clave con algoritmo SHA256."""
        email = "trainer@gym.com"
        password = "SecurePassword123!"
        
        mock_user_object = mock.Mock()
        mock_user_object.email = email
        mock_save_user.return_value = mock_user_object

        result= user_services.register_user(email, password, password)
        
        # Validar que se llamó al repositorio con la contraseña en SHA-256
        expected_hash = user_services.hash_password(password)
        mock_save_user.assert_called_once_with(email, expected_hash)
        self.assertIsNone(result)

    @patch('gym_app.repositories.user_repo.save_user')
    def test_register_user_invalid_email_raises(self, mock_save_user):
        """Verifica que un correo inválido lance ValueError y no intente guardar."""
        with self.assertRaises(ValueError) as context:
            user_services.register_user("bad-email", "Ab1!aaaa", "Ab1!aaaa")

        self.assertEqual(str(context.exception), "Correo electrónico no es válido.")
        mock_save_user.assert_not_called()

    @patch('gym_app.repositories.user_repo.save_user')
    def test_register_user_empty_fields_raises(self, mock_save_user):
        """Verifica que campos vacíos lancen ValueError y no se intente guardar."""
        with self.assertRaises(ValueError) as context:
            user_services.register_user("", "Ab1!aaaa", "Ab1!aaaa")

        self.assertEqual(str(context.exception), "Todos los campos son obligatorios.")
        mock_save_user.assert_not_called()

    @patch('gym_app.repositories.user_repo.save_user')
    def test_register_user_password_mismatch_raises(self, mock_save_user):
        """Verifica que contraseñas distintas lancen ValueError y no se intente guardar."""
        with self.assertRaises(ValueError) as context:
            user_services.register_user("user@test.com", "Ab1!aaaa", "Ab1!aaab")

        self.assertEqual(str(context.exception), "Las contraseñas no coinciden.")
        mock_save_user.assert_not_called()

    def test_register_user_invalid_password_raises(self):
        """Verifica que una contraseña insegura lance ValueError."""
        with self.assertRaises(ValueError) as context:
            user_services.register_user("user@test.com", "short", "short")

        self.assertEqual(str(context.exception), "La contraseña no cumple con los requisitos de seguridad.")

    @patch('gym_app.repositories.user_repo.fetch_user_by_email')
    def test_authenticate_user_wrong_password(self, mock_fetch_email):
        """Verifica que un usuario existente con clave errónea sea rechazado."""
        # Simular objeto de usuario devuelto por la BD
        mock_user = MagicMock()
        mock_user.password = user_services.hash_password("CorrectPass1!")
        
        mock_fetch_email.return_value = mock_user
        
        with self.assertRaises(ValueError) as context:
            user_services.authenticate_user("athlete1", "WrongPass2!")
            
        self.assertEqual(str(context.exception), "Contraseña incorrecta.")

    @patch('gym_app.repositories.user_repo.fetch_user_by_email')
    def test_authenticate_user_success_returns_user(self, mock_fetch_email):
        """Verifica que authenticate_user retorne el usuario cuando la contraseña es correcta."""
        mock_user = MagicMock()
        mock_user.password = user_services.hash_password("CorrectPass1!")
        mock_user.email = "athlete1@test.com"
        mock_fetch_email.return_value = mock_user

        result = user_services.authenticate_user("athlete1@test.com", "CorrectPass1!")
        self.assertIs(result, mock_user)
        self.assertEqual(result.email, "athlete1@test.com")

    @patch('gym_app.repositories.user_repo.fetch_user_by_email')
    def test_authenticate_user_not_found_raises(self, mock_fetch_email):
        """Verifica que un usuario inexistente lance ValueError."""
        mock_fetch_email.return_value = None

        with self.assertRaises(ValueError) as context:
            user_services.authenticate_user("missing@test.com", "AnyPass1!")

        self.assertEqual(str(context.exception), "Usuario no encontrado.")

    # -------------------------------------------------------------------------
    # CASO DE FALLO: El objetivo de entrenamiento no existe
    # -------------------------------------------------------------------------

    @mock.patch('gym_app.services.user_services.fetch_goal')
    def test_register_initial_data_invalid_goal_fails(self, mock_fetch_goal):
        """Verifica que si el objetivo del plan no se halla en la BD lance error."""
        # Arrange: Simulamos que el objetivo NO existe en la base de datos
        mock_fetch_goal.return_value = None  
        
        # Act & Assert: Validamos que dispare el ValueError con el mensaje correcto
        with self.assertRaises(ValueError) as context:
            user_services.register_initial_data(
                user_id=1, age=25, weight=70.0, goal_id=999, physical_test_data={"flexibilidad": 10}
            )
        self.assertEqual(str(context.exception), "El objetivo de entrenamiento no es válido.")

    @patch('gym_app.services.user_services.fetch_goal')
    def test_register_initial_data_invalid_age_raises(self, mock_fetch_goal):
        """Verifica que register_initial_data lance ValueError cuando la edad es inválida."""
        mock_fetch_goal.return_value = {"id": 1, "name": "Mantenimiento"}

        with self.assertRaises(ValueError) as context:
            user_services.register_initial_data(
                user_id=1, age=10, weight=70.0, goal_id=1, physical_test_data={"flexibilidad": 10}
            )
        self.assertEqual(str(context.exception), "La edad no cumple con el rango realista.")

    @patch('gym_app.services.user_services.fetch_goal')
    def test_register_initial_data_invalid_weight_raises(self, mock_fetch_goal):
        """Verifica que register_initial_data lance ValueError cuando el peso es inválido."""
        mock_fetch_goal.return_value = {"id": 1, "name": "Mantenimiento"}

        with self.assertRaises(ValueError) as context:
            user_services.register_initial_data(
                user_id=1, age=25, weight=10.0, goal_id=1, physical_test_data={"flexibilidad": 10}
            )
        self.assertEqual(str(context.exception), "El peso no cumple con el rango realista.")

    @mock.patch('gym_app.services.user_services.fetch_goal')
    @mock.patch('gym_app.services.user_services.fetch_latest_physical_test')
    @mock.patch('gym_app.services.user_services.fetch_user_profile')
    def test_update_user_data_invalid_age_raises(self, mock_fetch_profile, mock_fetch_test, mock_fetch_goal):
        """Verifica que update_user_data lance ValueError cuando la edad actualizada es inválida."""
        mock_original_profile = mock.Mock()
        mock_original_profile.age = 25
        mock_original_profile.weight = 70.0
        mock_original_profile.goal_id = 1
        mock_fetch_profile.return_value = mock_original_profile

        mock_original_test = mock.Mock()
        mock_original_test.results = {"flexibilidad": 4, "fuerza": 8}
        mock_fetch_test.return_value = mock_original_test

        mock_fetch_goal.return_value = {"id": 1, "name": "Mantenimiento"}

        with self.assertRaises(ValueError) as context:
            user_services.update_user_data(
                user_id=1, age=10, weight=70.0, goal_id=1, physical_test_data={"flexibilidad": 4}
            )

        self.assertEqual(str(context.exception), "La edad no cumple con el rango realista.")

    @mock.patch('gym_app.services.user_services.fetch_goal')
    @mock.patch('gym_app.services.user_services.fetch_latest_physical_test')
    @mock.patch('gym_app.services.user_services.fetch_user_profile')
    def test_update_user_data_invalid_weight_raises(self, mock_fetch_profile, mock_fetch_test, mock_fetch_goal):
        """Verifica que update_user_data lance ValueError cuando el peso actualizado es inválido."""
        mock_original_profile = mock.Mock()
        mock_original_profile.age = 25
        mock_original_profile.weight = 70.0
        mock_original_profile.goal_id = 1
        mock_fetch_profile.return_value = mock_original_profile

        mock_original_test = mock.Mock()
        mock_original_test.results = {"flexibilidad": 4, "fuerza": 8}
        mock_fetch_test.return_value = mock_original_test

        mock_fetch_goal.return_value = {"id": 1, "name": "Mantenimiento"}

        with self.assertRaises(ValueError) as context:
            user_services.update_user_data(
                user_id=1, age=25, weight=10.0, goal_id=1, physical_test_data={"flexibilidad": 4}
            )

        self.assertEqual(str(context.exception), "El peso no cumple con el rango realista.")

    # -------------------------------------------------------------------------
    # CASO DE ÉXITO: Todo fluye correctamente
    # -------------------------------------------------------------------------

    @mock.patch('gym_app.services.user_services.save_physical_test')
    @mock.patch('gym_app.services.user_services.save_user_profile')
    @mock.patch('gym_app.services.user_services.fetch_goal')
    def test_register_initial_data_success(self, mock_fetch_goal, mock_save_profile, mock_save_test):
        """Verifica el flujo correcto de registro de datos iniciales."""
        # 1. Arrange: Datos de entrada para la prueba
        user_id = 1
        age = 25
        weight = 70.0
        goal_id = 1
        physical_test_data = {"flexibilidad": 10, "fuerza": 5}
        
        # Simulamos que el objetivo SÍ existe para que pase la primera validación
        mock_fetch_goal.return_value = {"id": goal_id, "name": "Hipertrofia"}
        
        # EL TRUCO CLAVE: Creamos un mock para el perfil que retorna el modelo del ORM
        mock_profile_object = mock.Mock()
        mock_profile_object.id = 500  # Le inventamos un ID ficticio (ej. 500)
        
        # Le decimos a mock_save_profile que cuando lo llamen, devuelva este objeto con su .id
        mock_save_profile.return_value = mock_profile_object

        # 2. Act: Ejecutamos la función de tu servicio
        user_services.register_initial_data(user_id, age, weight, goal_id, physical_test_data)

        # 3. Assert: Verificaciones de comportamiento
        # Comprobamos que se intentó guardar el perfil con los parámetros correctos
        mock_save_profile.assert_called_once_with(user_id, age, weight, goal_id)
        
        # ¡ESTA ES LA LÍNEA MÁS IMPORTANTE!
        # Verificamos que save_physical_test recibió el ID del perfil ficticio (500) que creamos arriba
        mock_save_test.assert_called_once_with(500, physical_test_data)

    @patch('gym_app.repositories.user_repo.save_physical_test')
    @patch('gym_app.repositories.user_repo.save_user_profile')
    @patch('gym_app.repositories.validation_repo.fetch_goal')
    @patch('gym_app.repositories.user_repo.fetch_latest_physical_test')
    @patch('gym_app.repositories.user_repo.fetch_user_profile')
    def test_update_initial_data_partial_fill_success(self, mock_fetch_profile, mock_fetch_test, mock_fetch_goal, mock_save_profile, mock_save_test):
        """
        Caso de Éxito: Se envían algunos datos en None.
        Verifica que el servicio recupere los datos originales de la BD y actualice correctamente.
        """
        # 1. ARRANGEMENT (Preparar el escenario viejo en la BD)
        user_id = 1
        
        # Simulamos el perfil viejo que ya existía en la base de datos
        mock_original_profile = mock.Mock()
        mock_original_profile.age = 30
        mock_original_profile.weight = 85.0
        mock_original_profile.goal_id = 2
        mock_fetch_profile.return_value = mock_original_profile
        
        # Simulamos el test físico viejo que ya existía
        mock_original_test = mock.Mock()
        mock_original_test.results = {"flexibilidad": 4, "fuerza": 8}
        mock_fetch_test.return_value = mock_original_test
        
        # Simulamos que el objetivo que se va a validar SÍ existe
        mock_fetch_goal.return_value = {"id": 2, "name": "Definición"}
        
        # Simulamos el objeto perfil que retornará la función de guardado (ORM)
        mock_updated_profile = mock.Mock()
        mock_updated_profile.id = 777  # ID del perfil guardado
        mock_save_profile.return_value = mock_updated_profile

        # 2. ACT (Ejecutamos enviando datos mezclados: peso nuevo, pero edad y meta en None)
        # También enviamos physical_test_data como None para que use el viejo
        nuevo_peso = 80.0
        user_services.update_user_data(
            user_id=user_id, 
            age=None,          # Debería rescatar: 30
            weight=nuevo_peso, # Debería usar el nuevo: 80.0
            goal_id=None,      # Debería rescatar: 2
            physical_test_data=None # Debería rescatar: {"flexibilidad": 4, "fuerza": 8}
        )

        # 3. ASSERT (Verificaciones de comportamiento de la actualización)
        # Verificamos que save_user_profile se llamó con la MEZCLA de datos correcta
        mock_save_profile.assert_called_once_with(
            user_id, 
            30,          # Rescatado del perfil viejo
            nuevo_peso,  # El nuevo que ingresamos
            2            # Rescatado del perfil viejo
        )
        
        # Verificamos que save_physical_test heredó el ID del perfil (777) y los resultados viejos
        mock_save_test.assert_called_once_with(
            777, 
            {"flexibilidad": 4, "fuerza": 8} # Rescatado del test viejo
        )

    @mock.patch('gym_app.services.user_services.fetch_goal')
    @mock.patch('gym_app.services.user_services.fetch_latest_physical_test')
    @mock.patch('gym_app.services.user_services.fetch_user_profile')
    def test_update_initial_data_invalid_goal_fails(
        self, mock_fetch_profile, mock_fetch_test, mock_fetch_goal
    ):
        """
        Caso de Fallo: La meta (ya sea la nueva o la rescatada) no es válida.
        """
        # Arrange: El perfil original tenía la meta ID 999 (inválida por algún motivo)
        mock_original_profile = mock.Mock()
        mock_original_profile.age = 25
        mock_original_profile.weight = 70.0
        mock_original_profile.goal_id = 999
        mock_fetch_profile.return_value = mock_original_profile
        
        mock_original_test = mock.Mock()
        mock_original_test.results = {"resistencia": 10}
        mock_fetch_test.return_value = mock_original_test
        
        # Simulamos que fetch_goal no encuentra la meta en la BD
        mock_fetch_goal.return_value = None

        # Act & Assert: Al mandar goal_id=None, rescatará el 999, validará y debe estallar
        with self.assertRaises(ValueError) as context:
            user_services.update_user_data(
                user_id=1, age=25, weight=70.0, goal_id=None, physical_test_data={"resistencia": 10}
            )
        
        self.assertEqual(str(context.exception), "El objetivo de entrenamiento no es válido.")

        
    # ---------------------------------------------------------
    # TESTS FOR RF_6: Get User Routines
    # ---------------------------------------------------------

    @patch('gym_app.services.user_services.user_repo.fetch_user_routines')
    def test_get_user_routines_success(self, mock_fetch):
        """Edge Case: Valid user. Returns routine names from Rutine table JOIN."""
        # Arrange: Simulating the result of a JOIN between User_Rutine and Rutine
        mock_fetch.return_value = [
            {"routine_id": 1, "name": "Hypertrophy A"},
            {"routine_id": 2, "name": "Cardio Burn"}
        ]
        
        # Act
        result = user_services.get_user_routines_service(1)
        
        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], "Hypertrophy A")
        self.assertNotIn('Time', result[0], "Time attribute should not exist anymore.")
        mock_fetch.assert_called_once_with(1)

    @patch('gym_app.services.user_services.user_repo.fetch_user_routines')
    def test_get_user_routines_empty(self, mock_fetch):
        """Edge Case: Valid user but has no routines assigned."""
        mock_fetch.return_value = []
        result = user_services.get_user_routines_service(2)
        self.assertEqual(result, [])

    def test_get_user_routines_invalid_id(self):
        """Edge Case: Invalid ID type or value."""
        with self.assertRaises(ValueError):
            user_services.get_user_routines_service(-5)


    # ---------------------------------------------------------
    # TESTS FOR RF_8: Get Routine Exercises (Corrected Fields)
    # ---------------------------------------------------------
    @patch('gym_app.services.user_services.user_repo.fetch_routine_exercises')
    def test_get_routine_exercises_success(self, mock_fetch):
        """
        Edge Case: Valid routine. 
        Returns Series/Reps (Rutine_Exercise) and name/description (Exercise).
        """
        # Arrange: Mock represents fields combined from Rutine_Exercise and Exercise tables
        mock_fetch.return_value = [
            {
                "exercise_id": 5,
                "name": "Bench Press",         # From Exercise table
                "description": "Chest focus",   # From Exercise table
                "Series": 4,                    # From Rutine_Exercise table
                "Reps": 10                      # From Rutine_Exercise table
            }
        ]
        
        # Act
        result = user_services.get_routine_exercises_service(10)
        
        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], "Bench_Press" if False else "Bench Press")
        self.assertEqual(result[0]['description'], "Chest focus")
        self.assertEqual(result[0]['Series'], 4)
        self.assertEqual(result[0]['Reps'], 10)

    def test_get_routine_exercises_invalid_id(self):
        """Edge Case: Invalid routine ID."""
        with self.assertRaises(ValueError):
            user_services.get_routine_exercises_service(0)


    # ---------------------------------------------------------
    # TESTS FOR RF_9: Get User Profile (Security Filter)
    # ---------------------------------------------------------
    @patch('gym_app.services.user_services.user_repo.fetch_user_profile')
    def test_get_user_profile_success_strips_password(self, mock_fetch):
        """Edge Case: Ensure sensitive data (password) is removed."""
        mock_fetch.return_value = {
            "name": "John Doe",
            "age": 25,
            "weight": 80.5,
            "email": "john@example.com",
            "password": "hashed_password_123", 
            "goal_id": 1
        }
        
        result = user_services.get_user_profile_service(1)
        
        self.assertEqual(result["name"], "John Doe")
        self.assertNotIn("password", result)

    @patch('gym_app.services.user_services.user_repo.fetch_user_profile')
    def test_get_user_profile_not_found(self, mock_fetch):
        """Edge Case: User does not exist."""
        mock_fetch.return_value = None
        with self.assertRaises(ValueError):
            user_services.get_user_profile_service(999)

if __name__ == '__main__':
    unittest.main()