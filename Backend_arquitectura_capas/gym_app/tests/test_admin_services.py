import unittest
from unittest.mock import patch
from services.admin_services import no_invalid_chars, valid_name_length, register_machine

class TestMachineValidator(unittest.TestCase):

    # ==========================
    # Tests de no_invalid_chars
    # ==========================

    def test_no_invalid_chars_valid_name(self):
        self.assertTrue(no_invalid_chars("PressBanca"))
        self.assertTrue(valid_name_length("Caminadora"))
        self.assertTrue(valid_name_length("Maquina123"))

    def test_no_invalid_chars_invalid_name(self):
        self.assertFalse(no_invalid_chars("Press!Banca"))
        self.assertFalse(no_invalid_chars("Caminadora@"))
        self.assertFalse(no_invalid_chars("Maquina#1"))

    # ==========================
    # Tests de valid_name_length
    # ==========================

    def test_valid_name_length_minimum(self):
        self.assertTrue(valid_name_length("A"))

    def test_valid_name_length_maximum(self):
        self.assertTrue(valid_name_length("A" * 50))

    def test_valid_name_length_empty(self):
        self.assertFalse(valid_name_length(""))

    def test_valid_name_length_too_long(self):
        self.assertFalse(valid_name_length("A" * 51))

    # ==========================
    # Tests de register_machine
    # ==========================

    @patch("gym_app.services.admin_services.admin_repo.machine_name_exists")
    def test_register_machine_valid(self, mock_exists):
        mock_exists.return_value = False

        result = register_machine(
            "PressBanca",
            "CHEST"
        )

        self.assertTrue(result)

    @patch("gym_app.services.admin_services.admin_repo.machine_name_exists")
    def test_register_machine_invalid_chars(self, mock_exists):
        mock_exists.return_value = False

        with self.assertRaises(ValueError) as context:
            register_machine(
                "Press!Banca",
                "CHEST"
            )

        self.assertEqual(
            str(context.exception),
            "El nombre de la máquina contiene caracteres no permitidos."
        )

    @patch("gym_app.services.admin_services.admin_repo.machine_name_exists")
    def test_register_machine_invalid_length(self, mock_exists):
        mock_exists.return_value = False

        with self.assertRaises(ValueError) as context:
            register_machine(
                "",
                "CHEST"
            )

        self.assertEqual(
            str(context.exception),
            "El nombre de la máquina debe tener entre 1 y 50 caracteres."
        )

    @patch("gym_app.services.admin_services.admin_repo.machine_name_exists")
    def test_register_machine_invalid_area(self, mock_exists):
        mock_exists.return_value = False

        with self.assertRaises(ValueError) as context:
            register_machine(
                "PressBanca",
                "HOMBROS"
            )

        self.assertEqual(
            str(context.exception),
            "Área corporal no elegida."
        )

    @patch("gym_app.services.admin_services.admin_repo.machine_name_exists")
    def test_register_machine_duplicate_name(self, mock_exists):
        mock_exists.return_value = True

        with self.assertRaises(ValueError) as context:
            register_machine(
                "PressBanca",
                "CHEST"
            )

        self.assertEqual(
            str(context.exception),
            "Ya existe una máquina con ese nombre."
        )


if __name__ == "__main__":
    unittest.main()