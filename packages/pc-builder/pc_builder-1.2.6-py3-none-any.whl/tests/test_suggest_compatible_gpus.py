import unittest
from unittest.mock import MagicMock, patch
from pc_builder.suggestions.gpu import suggestCompatibleGPUs


class TestSuggestCompatibleGPUs(unittest.TestCase):

    @patch("pc_builder.components.gpu.loadGPUsfromJSON")
    def test_suggest_compatible_gpus(self, mock_load_gpus):
        """Testing if the function correctly filters out incompatible gpus."""

        gpu1 = MagicMock()
        gpu1.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
        gpu1.price = "200$"

        gpu2 = MagicMock()
        gpu2.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
        gpu2.price = "200$"

        gpu3 = MagicMock()
        gpu3.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))
        gpu3.price = "200$"

        mock_load_gpus.return_value = [gpu1, gpu2, gpu3]

        userBuild = MagicMock()
        userBuild.budget = 1500.0
        userBuild.useCase = "work"
        userBuild.totalPrice = 500.0

        result = suggestCompatibleGPUs(userBuild, gpuComp=None)

        self.assertEqual(len(result), 2)
        self.assertIn(gpu1, result)
        self.assertIn(gpu2, result)
        self.assertNotIn(gpu3, result)

    @patch("pc_builder.components.gpu.loadGPUsfromJSON")
    def test_suggest_compatible_gpus_limit_results(self, mock_load_gpus):
        """Testing if the function returns no more than 5 compatible gpus."""

        compatible_gpus = [MagicMock() for _ in range(10)]
        for gpu in compatible_gpus:
            gpu.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
            gpu.price = "200$"

        mock_load_gpus.return_value = compatible_gpus

        userBuild = MagicMock()
        userBuild.budget = 1500.0
        userBuild.useCase = "work"
        userBuild.totalPrice = 500.0

        result = suggestCompatibleGPUs(userBuild, gpuComp=None)

        self.assertEqual(len(result), 5)
        for gpu in compatible_gpus[:5]:
            self.assertIn(gpu, result)

    @patch("pc_builder.components.gpu.loadGPUsfromJSON")
    def test_suggest_compatible_gpus_no_compatible_found(self, mock_load_gpus):
        """Testing if the function returns an empty list when no compatible gpus are found."""

        gpu1 = MagicMock()
        gpu1.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))
        gpu1.price = "200$"

        gpu2 = MagicMock()
        gpu2.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))
        gpu2.price = "200$"

        mock_load_gpus.return_value = [gpu1, gpu2]

        userBuild = MagicMock()
        userBuild.budget = 1500.0
        userBuild.useCase = "work"
        userBuild.totalPrice = 500.0

        result = suggestCompatibleGPUs(userBuild, gpuComp=None)

        self.assertEqual(len(result), 0)


class TestSuggestCompatibleGPUsExtended(unittest.TestCase):

    @patch("pc_builder.components.gpu.loadGPUsfromJSON")
    def test_out_of_budget_returns_cheapest_gpus(self, mock_load_gpus):
        """Testing if out of budget returns only the top 5 cheapest compatible GPUs."""

        gpu1 = MagicMock(
            price="230$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        gpu2 = MagicMock(
            price="250$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        gpu3 = MagicMock(
            price="240$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        gpu4 = MagicMock(
            price="220$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        gpu5 = MagicMock(
            price="300$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        gpu6 = MagicMock(
            price="210$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )

        mock_load_gpus.return_value = [
            gpu1,
            gpu2,
            gpu3,
            gpu4,
            gpu5,
            gpu6,
        ]

        userBuild = MagicMock()
        userBuild.budget = 1000.0
        userBuild.useCase = "work"
        userBuild.totalPrice = 1001.0

        result = suggestCompatibleGPUs(userBuild, gpuComp=None)

        self.assertEqual(len(result), 5)
        self.assertIn(gpu6, result)
        self.assertNotIn(gpu5, result)

    @patch("pc_builder.components.gpu.loadGPUsfromJSON")
    def test_gpu_within_budget_and_use_case_work(self, mock_load_gpus):
        """Testing if gpus are filtered correctly within budget and based on use case."""

        gpu1 = MagicMock(
            price="299$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        gpu2 = MagicMock(
            price="300$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        gpu3 = MagicMock(
            price="301$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )

        mock_load_gpus.return_value = [gpu1, gpu2, gpu3]

        userBuild = MagicMock()
        userBuild.budget = 1000.0
        userBuild.useCase = "work"
        userBuild.totalPrice = 600.0

        result = suggestCompatibleGPUs(userBuild, gpuComp=None)

        self.assertEqual(len(result), 2)
        self.assertIn(gpu1, result)
        self.assertIn(gpu2, result)
        self.assertNotIn(gpu3, result)

    @patch("pc_builder.components.gpu.loadGPUsfromJSON")
    def test_gpu_within_budget_and_use_case_gaming(self, mock_load_gpus):
        """Testing if gpus are filtered correctly within budget and based on use case."""

        gpu1 = MagicMock(
            price="349$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        gpu2 = MagicMock(
            price="350$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        gpu3 = MagicMock(
            price="351$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )

        mock_load_gpus.return_value = [gpu1, gpu2, gpu3]

        userBuild = MagicMock()
        userBuild.budget = 1000.0
        userBuild.useCase = "gaming"
        userBuild.totalPrice = 600.0

        result = suggestCompatibleGPUs(userBuild, gpuComp=None)

        self.assertEqual(len(result), 2)
        self.assertIn(gpu1, result)
        self.assertIn(gpu2, result)
        self.assertNotIn(gpu3, result)

    @patch("pc_builder.components.gpu.loadGPUsfromJSON")
    def test_gpu_exceeding_remaining_build_budget(self, mock_load_gpus):
        """Testing if gpus exceeding remaining total budget are excluded."""

        gpu1 = MagicMock(
            price="299$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        gpu2 = MagicMock(
            price="300$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        gpu3 = MagicMock(
            price="301$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )

        mock_load_gpus.return_value = [gpu1, gpu2, gpu3]

        userBuild = MagicMock()
        userBuild.budget = 1000.0
        userBuild.useCase = "work"
        userBuild.totalPrice = 701.0  # 299 is max price of gpu

        result = suggestCompatibleGPUs(userBuild, gpuComp=None)

        self.assertEqual(len(result), 1)
        self.assertIn(gpu1, result)
        self.assertNotIn(gpu2, result)
        self.assertNotIn(gpu3, result)
