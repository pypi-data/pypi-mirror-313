import unittest
from unittest.mock import MagicMock, patch
from pc_builder.suggestions.ram import suggestCompatibleRAMs


class TestSuggestCompatibleRAMs(unittest.TestCase):

    @patch("pc_builder.components.ram.loadRAMsfromJSON")
    def test_suggest_compatible_rams(self, mock_load_rams):
        """Testing if the function correctly filters out incompatible RAMs."""

        ram1 = MagicMock()
        ram1.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
        ram1.price = "60$"

        ram2 = MagicMock()
        ram2.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
        ram2.price = "60$"

        ram3 = MagicMock()
        ram3.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))
        ram3.price = "60$"

        mock_load_rams.return_value = [ram1, ram2, ram3]

        userBuild = MagicMock()
        userBuild.budget = 1000  # Set a valid budget
        userBuild.totalPrice = 500  # Set current total build cost
        userBuild.useCase = "work"  # Set use case
        userBuild.components = {"ram": []}  # Assume no RAM in the current build

        result = suggestCompatibleRAMs(userBuild, ramComp=None)

        self.assertEqual(len(result), 2)
        self.assertIn(ram1, result)
        self.assertIn(ram2, result)
        self.assertNotIn(ram3, result)

    @patch("pc_builder.components.ram.loadRAMsfromJSON")
    def test_suggest_compatible_rams_limit_results(self, mock_load_rams):
        """Testing if the function returns no more than 5 compatible RAMs."""

        compatible_rams = [MagicMock() for _ in range(10)]
        for ram in compatible_rams:
            ram.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
            ram.price = "60$"

        mock_load_rams.return_value = compatible_rams

        userBuild = MagicMock()
        userBuild.budget = 1000  # Set a valid budget
        userBuild.totalPrice = 500  # Set current total build cost
        userBuild.useCase = "work"  # Set use case
        userBuild.components = {"ram": []}  # Assume no RAM in the current build

        result = suggestCompatibleRAMs(userBuild, ramComp=None)

        self.assertEqual(len(result), 5)
        for ram in compatible_rams[:5]:
            self.assertIn(ram, result)

    @patch("pc_builder.components.ram.loadRAMsfromJSON")
    def test_suggest_compatible_rams_no_compatible_found(self, mock_load_rams):
        """Testing if the function returns an empty list when no compatible RAMs are found."""

        ram1 = MagicMock()
        ram1.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))
        ram1.price = "60$"

        ram2 = MagicMock()
        ram2.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))
        ram2.price = "60$"

        mock_load_rams.return_value = [ram1, ram2]

        userBuild = MagicMock()
        userBuild.budget = 1000  # Set a valid budget
        userBuild.totalPrice = 500  # Set current total build cost
        userBuild.useCase = "work"  # Set use case
        userBuild.components = {"ram": []}  # Assume no RAM in the current build

        result = suggestCompatibleRAMs(userBuild, ramComp=None)

        self.assertEqual(len(result), 0)


class TestSuggestCompatibleRAMsExtended(unittest.TestCase):

    @patch("pc_builder.components.ram.loadRAMsfromJSON")
    def test_out_of_budget_returns_cheapest_rams(self, mock_load_rams):
        """Testing if out of budget returns only the top 5 cheapest compatible RAMs."""

        ram1 = MagicMock(
            price="20$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        ram2 = MagicMock(
            price="15$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        ram3 = MagicMock(
            price="25$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        ram4 = MagicMock(
            price="10$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        ram5 = MagicMock(
            price="30$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        ram6 = MagicMock(
            price="5$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )

        mock_load_rams.return_value = [ram1, ram2, ram3, ram4, ram5, ram6]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.useCase = "gaming"  # Not relevant for zero budget
        userBuild.totalPrice = 1100
        userBuild.components = {}

        result = suggestCompatibleRAMs(userBuild, ramComp=None)

        self.assertEqual(len(result), 5)
        self.assertIn(ram6, result)
        self.assertNotIn(ram5, result)

    @patch("pc_builder.components.ram.loadRAMsfromJSON")
    def test_rams_within_budget_and_use_case_work(self, mock_load_rams):
        """Testing if RAMs are filtered correctly within budget and based on use case."""

        ram1 = MagicMock(
            price="50$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        ram2 = MagicMock(
            price="100$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        ram3 = MagicMock(
            price="200$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )

        mock_load_rams.return_value = [ram1, ram2, ram3]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.useCase = "work"
        userBuild.totalPrice = 700  # Leaves 300 for components and 100 for RAMs
        userBuild.components = {"ram": []}

        result = suggestCompatibleRAMs(userBuild, ramComp=None)

        self.assertIn(ram1, result)  # Within budget
        self.assertIn(ram2, result)  # Within budget
        self.assertNotIn(ram3, result)  # Exceeds budget for RAM

    @patch("pc_builder.components.ram.loadRAMsfromJSON")
    def test_rams_within_budget_and_use_case_gaming(self, mock_load_rams):
        """Testing if RAMs are filtered correctly within budget and based on use case."""

        ram1 = MagicMock(
            price="80$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        ram2 = MagicMock(
            price="100$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        ram3 = MagicMock(
            price="200$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )

        mock_load_rams.return_value = [ram1, ram2, ram3]

        userBuild = MagicMock()
        userBuild.budget = 1000.0
        userBuild.useCase = "gaming"
        userBuild.totalPrice = 700.0  # Leaves 300 for components and 80 for RAMs
        userBuild.components = {"ram": []}

        result = suggestCompatibleRAMs(userBuild, ramComp=None)

        self.assertIn(ram1, result)  # Within budget
        self.assertNotIn(ram2, result)  # Exceeds budget for RAM
        self.assertNotIn(ram3, result)  # Exceeds budget for RAM

    @patch("pc_builder.components.ram.loadRAMsfromJSON")
    def test_rams_exceeding_remaining_build_budget(self, mock_load_rams):
        """Testing if RAMs exceeding remaining total budget are excluded."""

        ram1 = MagicMock(
            price="50$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        ram2 = MagicMock(
            price="100$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        ram3 = MagicMock(
            price="150$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )

        mock_load_rams.return_value = [ram1, ram2, ram3]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.useCase = "gaming"
        userBuild.totalPrice = 950  # Only 50 remaining
        userBuild.components = {}

        result = suggestCompatibleRAMs(userBuild, ramComp=None)

        self.assertEqual(len(result), 1)
        self.assertIn(ram1, result)  # Only RAM within remaining budget
        self.assertNotIn(ram2, result)  # Exceeds remaining budget
        self.assertNotIn(ram3, result)

    @patch("pc_builder.components.ram.loadRAMsfromJSON")
    def test_included_existing_ram_cost_work(self, mock_load_rams):
        """Testing if existing RAM cost is factored into remaining RAM budget."""

        existing_ram = MagicMock(
            price="60$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        newRam1 = MagicMock(
            price="40$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        newRam2 = MagicMock(
            price="41$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )

        mock_load_rams.return_value = [newRam1, newRam2]

        userBuild = MagicMock()
        userBuild.budget = 1000.0
        userBuild.useCase = "work"
        userBuild.totalPrice = 900.0
        userBuild.components = {"ram": [existing_ram]}  # Already spent $60 on RAM

        result = suggestCompatibleRAMs(userBuild, ramComp=None)

        self.assertEqual(len(result), 1)
        self.assertIn(newRam1, result)  # Only fits in remaining budget
        self.assertNotIn(newRam2, result)  # Exceeds remaining budget

    @patch("pc_builder.components.ram.loadRAMsfromJSON")
    def test_included_existing_ram_cost_gaming(self, mock_load_rams):
        """Testing if existing RAM cost is factored into remaining RAM budget."""

        existing_ram = MagicMock(
            price="60$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        newRam1 = MagicMock(
            price="20$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        newRam2 = MagicMock(
            price="21$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )

        mock_load_rams.return_value = [newRam1, newRam2]

        userBuild = MagicMock()
        userBuild.budget = 1000.0
        userBuild.useCase = "gaming"
        userBuild.totalPrice = 900.0
        userBuild.components = {"ram": [existing_ram]}  # Already spent $60 on RAM

        result = suggestCompatibleRAMs(userBuild, ramComp=None)

        self.assertEqual(len(result), 1)
        self.assertIn(newRam1, result)  # Only fits in remaining budget
        self.assertNotIn(newRam2, result)  # Exceeds remaining budget
