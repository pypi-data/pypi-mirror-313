import unittest
from unittest.mock import MagicMock, patch
from pc_builder.suggestions.cpu import suggestCompatibleCPUs


class TestsuggestCompatibleCPUs(unittest.TestCase):

    @patch("pc_builder.components.cpu.loadCPUsfromJSON")
    def test_suggest_compatible_cpus(self, mock_load_cpus):
        """Testing if the function correctly filters out incompatible CPUs."""

        cpu1 = MagicMock()
        cpu1.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
        cpu1.price = "200$"

        cpu2 = MagicMock()
        cpu2.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
        cpu2.price = "250$"

        cpu3 = MagicMock()
        cpu3.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))
        cpu3.price = "300$"

        mock_load_cpus.return_value = [cpu1, cpu2, cpu3]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.useCase = "gaming"
        userBuild.totalPrice = 800
        userBuild.components = {"cpu": []}  # Assume no CPU in the current build

        result = suggestCompatibleCPUs(userBuild, cpuComp=None)

        self.assertEqual(len(result), 1)
        self.assertIn(result[0], [cpu1])
        self.assertNotIn(cpu3, result)

    @patch("pc_builder.components.cpu.loadCPUsfromJSON")
    def test_suggest_compatible_cpus_limit_results(self, mock_load_cpus):
        """Testing if the function returns no more than 5 CPUs."""

        compatible_cpus = [MagicMock() for _ in range(10)]
        for cpu in compatible_cpus:
            cpu.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
            cpu.price = "250$"

        mock_load_cpus.return_value = compatible_cpus

        userBuild = MagicMock()
        userBuild.budget = 2000
        userBuild.totalPrice = 1600
        userBuild.useCase = "work"
        userBuild.components = {"cpu": []}

        result = suggestCompatibleCPUs(userBuild, cpuComp=None)

        self.assertEqual(len(result), 5)
        for cpu in compatible_cpus[:5]:
            self.assertIn(cpu, result)

    @patch("pc_builder.components.cpu.loadCPUsfromJSON")
    def test_suggest_compatible_cpus_no_compatible_found(self, mock_load_cpus):
        """Testing when no compatible CPUs are found."""

        cpu1 = MagicMock(
            checkCompatibility=MagicMock(return_value=(False, "Incompatible")),
            price="200$",
        )
        cpu2 = MagicMock(
            checkCompatibility=MagicMock(return_value=(False, "Incompatible")),
            price="250$",
        )
        cpu3 = MagicMock(
            checkCompatibility=MagicMock(return_value=(False, "Incompatible")),
            price="300$",
        )

        mock_load_cpus.return_value = [cpu1, cpu2, cpu3]

        userBuild = MagicMock()
        userBuild.budget = 1500
        userBuild.totalPrice = 1200
        userBuild.components = {"cpu": []}  # Assume no CPU in the current build

        result = suggestCompatibleCPUs(userBuild, cpuComp=None)

        self.assertEqual(len(result), 0)  # Expect no compatible CPUs in the result


class TestsuggestCompatibleCPUsExtended(unittest.TestCase):

    @patch("pc_builder.components.cpu.loadCPUsfromJSON")
    def test_out_of_budget_returns_cheapest_cpus(self, mock_load_cpus):
        """Testing if out of budget returns only the top 5 cheapest compatible CPUs."""

        cpu1 = MagicMock(
            price="150$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        cpu2 = MagicMock(
            price="120$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        cpu3 = MagicMock(
            price="170$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        cpu4 = MagicMock(
            price="110$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        cpu5 = MagicMock(
            price="190$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        cpu6 = MagicMock(
            price="100$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )

        mock_load_cpus.return_value = [cpu1, cpu2, cpu3, cpu4, cpu5, cpu6]

        userBuild = MagicMock()
        userBuild.budget = 2000
        userBuild.totalPrice = 2100  # Budget exceeded
        userBuild.components = {"cpu": []}

        result = suggestCompatibleCPUs(userBuild, cpuComp=None)

        self.assertEqual(len(result), 5)
        self.assertIn(cpu6, result)
        self.assertNotIn(cpu5, result)

    @patch("pc_builder.components.cpu.loadCPUsfromJSON")
    def test_cpus_within_budget_and_use_case_work(self, mock_load_cpus):
        """Testing if CPUs are filtered correctly within budget and based on work use case."""

        cpu1 = MagicMock(
            price="230$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        cpu2 = MagicMock(
            price="500$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        cpu3 = MagicMock(
            price="510$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )

        mock_load_cpus.return_value = [cpu1, cpu2, cpu3]

        userBuild = MagicMock()
        userBuild.budget = 2000
        userBuild.useCase = "work"
        userBuild.totalPrice = 1600
        userBuild.components = {"cpu": []}

        result = suggestCompatibleCPUs(userBuild, cpuComp=None)

        self.assertIn(cpu1, result)  # Within budget (20% of 2000 = 400)
        self.assertNotIn(cpu2, result)  # Exceeds budget for CPU (20% of 2000 = 400)
        self.assertNotIn(cpu3, result)  # Exceeds budget for CPU (20% of 2000 = 400)

    @patch("pc_builder.components.cpu.loadCPUsfromJSON")
    def test_cpus_within_budget_and_use_case_gaming(self, mock_load_cpus):
        """Testing if CPUs are filtered correctly within budget and based on gaming use case."""

        cpu1 = MagicMock(
            price="200$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        cpu2 = MagicMock(
            price="500$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        cpu3 = MagicMock(
            price="600$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )

        mock_load_cpus.return_value = [cpu1, cpu2, cpu3]

        userBuild = MagicMock()
        userBuild.budget = 2000
        userBuild.useCase = "gaming"
        userBuild.totalPrice = 1500
        userBuild.components = {"cpu": []}

        result = suggestCompatibleCPUs(userBuild, cpuComp=None)

        self.assertEqual(len(result), 1)
        self.assertIn(cpu1, result)  # Within budget (20% of 2000 = 400)
        self.assertNotIn(cpu2, result)  # Within budget (20% of 2000 = 400)
        self.assertNotIn(cpu3, result)  # Exceeds budget for CPU

    @patch("pc_builder.components.cpu.loadCPUsfromJSON")
    def test_cpu_exceeding_remaining_build_budget(self, mock_load_cpus):
        """Testing if CPUs exceeding the remaining total budget are excluded."""

        cpu1 = MagicMock(
            price="199$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        cpu2 = MagicMock(
            price="200$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        cpu3 = MagicMock(
            price="201$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )

        mock_load_cpus.return_value = [cpu1, cpu2, cpu3]

        userBuild = MagicMock()
        userBuild.budget = 1000.0
        userBuild.useCase = "work"
        userBuild.totalPrice = 801.0  # 200 is the max price for the CPU (20% of 1000)

        result = suggestCompatibleCPUs(userBuild, cpuComp=None)

        self.assertEqual(len(result), 1)
        self.assertIn(cpu1, result)
        self.assertNotIn(cpu2, result)
        self.assertNotIn(cpu3, result)
