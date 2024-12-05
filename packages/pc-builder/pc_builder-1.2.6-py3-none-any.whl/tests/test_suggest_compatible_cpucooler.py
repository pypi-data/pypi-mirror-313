import unittest
from unittest.mock import MagicMock, patch
from pc_builder.suggestions.cpucooler import suggestCompatibleCPUcoolers


class TestsuggestCompatibleCPUcoolers(unittest.TestCase):

    @patch("pc_builder.components.cpucooler.loadCPUCoolersfromJSON")
    def test_suggest_compatible_cpucoolers(self, mock_load_cpucoolers):
        """Testing if the function correctly filters out incompatible CPU coolers."""

        cooler1 = MagicMock()
        cooler1.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
        cooler1.price = "50$"

        cooler2 = MagicMock()
        cooler2.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
        cooler2.price = "60$"

        cooler3 = MagicMock()
        cooler3.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))
        cooler3.price = "70$"

        mock_load_cpucoolers.return_value = [cooler1, cooler2, cooler3]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.useCase = "work"
        userBuild.totalPrice = 500
        userBuild.components = {
            "cpucooler": []
        }  # Assume no CPU cooler in the current build

        result = suggestCompatibleCPUcoolers(userBuild, cpuCoolerComp=None)

        self.assertEqual(len(result), 1)
        self.assertIn(result[0], [cooler1])
        self.assertNotIn(cooler3, result)

    @patch("pc_builder.components.cpucooler.loadCPUCoolersfromJSON")
    def test_suggest_compatible_cpucoolers_limit_results(self, mock_load_cpucoolers):
        """Testing if the function returns no more than 5 CPU coolers."""

        compatible_coolers = [MagicMock() for _ in range(10)]
        for cooler in compatible_coolers:
            cooler.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
            cooler.price = "60$"

        mock_load_cpucoolers.return_value = compatible_coolers

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.totalPrice = 500
        userBuild.useCase = "work"
        userBuild.components = {"cpucooler": []}

        result = suggestCompatibleCPUcoolers(userBuild, cpuCoolerComp=None)

        self.assertEqual(len(result), 5)
        for cooler in compatible_coolers[:5]:
            self.assertIn(cooler, result)

    @patch("pc_builder.components.cpucooler.loadCPUCoolersfromJSON")
    def test_suggest_compatible_cpucoolers_no_compatible_found(
        self, mock_load_cpucoolers
    ):
        """Testing when no compatible CPU coolers are found."""

        cooler1 = MagicMock(
            checkCompatibility=MagicMock(return_value=(False, "Incompatible")),
            price="50$",
        )
        cooler2 = MagicMock(
            checkCompatibility=MagicMock(return_value=(False, "Incompatible")),
            price="60$",
        )
        cooler3 = MagicMock(
            checkCompatibility=MagicMock(return_value=(False, "Incompatible")),
            price="70$",
        )

        mock_load_cpucoolers.return_value = [cooler1, cooler2, cooler3]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.totalPrice = 600
        userBuild.components = {
            "cpucooler": []
        }  # Assume no CPU cooler in the current build

        result = suggestCompatibleCPUcoolers(userBuild, cpuCoolerComp=None)

        self.assertEqual(
            len(result), 0
        )  # Expect no compatible CPU coolers in the result


class TestsuggestCompatibleCPUcoolerssExtended(unittest.TestCase):

    @patch("pc_builder.components.cpucooler.loadCPUCoolersfromJSON")
    def test_out_of_budget_returns_cheapest_cpucoolers(self, mock_load_cpucoolers):
        """Testing if out of budget returns only the top 5 cheapest compatible CPU coolers."""

        cooler1 = MagicMock(
            price="20$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        cooler2 = MagicMock(
            price="15$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        cooler3 = MagicMock(
            price="25$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        cooler4 = MagicMock(
            price="10$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        cooler5 = MagicMock(
            price="30$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        cooler6 = MagicMock(
            price="5$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )

        mock_load_cpucoolers.return_value = [
            cooler1,
            cooler2,
            cooler3,
            cooler4,
            cooler5,
            cooler6,
        ]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.totalPrice = 1100  # Budget exceeded
        userBuild.components = {"cpucooler": []}

        result = suggestCompatibleCPUcoolers(userBuild, cpuCoolerComp=None)

        self.assertEqual(len(result), 5)
        self.assertIn(cooler6, result)
        self.assertNotIn(cooler5, result)

    @patch("pc_builder.components.cpucooler.loadCPUCoolersfromJSON")
    def test_cpucoolers_within_budget_and_use_case_work(self, mock_load_cpucoolers):
        """Testing if CPU coolers are filtered correctly within budget and based on work use case."""

        cooler1 = MagicMock(
            price="50$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        cooler2 = MagicMock(
            price="120$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        cooler3 = MagicMock(
            price="130$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )

        mock_load_cpucoolers.return_value = [cooler1, cooler2, cooler3]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.useCase = "work"
        userBuild.totalPrice = 500
        userBuild.components = {"cpucooler": []}

        result = suggestCompatibleCPUcoolers(userBuild, cpuCoolerComp=None)

        self.assertIn(cooler1, result)  # Within budget
        self.assertNotIn(cooler2, result)  # Exceeds budget for CPU cooler
        self.assertNotIn(cooler3, result)  # Exceeds budget for CPU cooler

    @patch("pc_builder.components.cpucooler.loadCPUCoolersfromJSON")
    def test_cpucoolers_within_budget_and_use_case_gaming(self, mock_load_cpucoolers):
        """Testing if CPU coolers are filtered correctly within budget and based on gaming use case."""

        cooler1 = MagicMock(
            price="35$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        cooler2 = MagicMock(
            price="40$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        cooler3 = MagicMock(
            price="75$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )

        mock_load_cpucoolers.return_value = [cooler1, cooler2, cooler3]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.useCase = "gaming"
        userBuild.totalPrice = 960
        userBuild.components = {"cpucooler": []}

        result = suggestCompatibleCPUcoolers(userBuild, cpuCoolerComp=None)

        self.assertEqual(len(result), 2)
        self.assertIn(cooler1, result)  # Within budget
        self.assertIn(cooler2, result)  # Within budget
        self.assertNotIn(cooler3, result)  # Exceeds budget

    @patch("pc_builder.components.cpucooler.loadCPUCoolersfromJSON")
    def test_cpucooler_exceeding_remaining_build_budget(self, mock_load_cpucoolers):
        """Testing if CPU coolers exceeding the remaining total budget are excluded."""

        # Mocking CPU cooler objects
        cooler1 = MagicMock(
            price="49$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        cooler2 = MagicMock(
            price="50$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        cooler3 = MagicMock(
            price="51$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )

        mock_load_cpucoolers.return_value = [cooler1, cooler2, cooler3]

        # Mocking user build
        userBuild = MagicMock()
        userBuild.budget = 1000.0
        userBuild.useCase = "work"
        userBuild.totalPrice = (
            951.0  # 49 is the max price for the CPU cooler (5% of 1000)
        )

        # Suggest compatible CPU coolers
        result = suggestCompatibleCPUcoolers(userBuild, cpuCoolerComp=None)

        # Validating results
        self.assertEqual(len(result), 1)
        self.assertIn(cooler1, result)
        self.assertNotIn(cooler2, result)
        self.assertNotIn(cooler3, result)
