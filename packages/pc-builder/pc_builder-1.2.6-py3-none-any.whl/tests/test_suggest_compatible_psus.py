import unittest
from unittest.mock import MagicMock, patch
from pc_builder.suggestions.psu import suggestCompatiblePSUs


class TestSuggestCompatiblePSUs(unittest.TestCase):

    @patch("pc_builder.components.psu.loadPSUsfromJSON")
    def test_suggest_compatible_psus(self, mock_load_psus):
        """Testing if the function correctly filters out incompatible psus."""

        psu1 = MagicMock()
        psu1.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
        psu1.price = "90$"

        psu2 = MagicMock()
        psu2.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
        psu2.price = "90$"

        psu3 = MagicMock()
        psu3.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))
        psu3.price = "90$"

        mock_load_psus.return_value = [psu1, psu2, psu3]

        userBuild = MagicMock()
        userBuild.budget = 1200.0
        userBuild.totalPrice = 400.0

        result = suggestCompatiblePSUs(userBuild, psuComp=None)

        self.assertEqual(len(result), 2)
        self.assertIn(psu1, result)
        self.assertIn(psu2, result)
        self.assertNotIn(psu3, result)

    @patch("pc_builder.components.psu.loadPSUsfromJSON")
    def test_suggest_compatible_psus_limit_results(self, mock_load_psus):
        """Testing if the function returns no more than 5 compatible psus."""

        compatible_psus = [MagicMock() for _ in range(10)]
        for psu in compatible_psus:
            psu.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
            psu.price = "90$"

        mock_load_psus.return_value = compatible_psus

        userBuild = MagicMock()
        userBuild.budget = 1200.0
        userBuild.totalPrice = 400.0

        result = suggestCompatiblePSUs(userBuild, psuComp=None)

        self.assertEqual(len(result), 5)
        for psu in compatible_psus[:5]:
            self.assertIn(psu, result)

    @patch("pc_builder.components.psu.loadPSUsfromJSON")
    def test_suggest_compatible_psus_no_compatible_found(self, mock_load_psus):
        """Testing if the function returns an empty list when no compatible psus are found."""

        psu1 = MagicMock()
        psu1.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))
        psu1.price = "90$"

        psu2 = MagicMock()
        psu2.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))
        psu2.price = "90$"

        mock_load_psus.return_value = [psu1, psu2]

        userBuild = MagicMock()
        userBuild.budget = 1200.0
        userBuild.totalPrice = 400.0

        result = suggestCompatiblePSUs(userBuild, psuComp=None)

        self.assertEqual(len(result), 0)


class TestSuggestCompatiblePSUsExtended(unittest.TestCase):

    @patch("pc_builder.components.psu.loadPSUsfromJSON")
    def test_out_of_budget_returns_cheapest_psus(self, mock_load_psus):
        """Testing if out of budget returns only the top 5 cheapest compatible PSUs."""

        psu1 = MagicMock(
            price="85$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        psu2 = MagicMock(
            price="80$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        psu3 = MagicMock(
            price="100$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        psu4 = MagicMock(
            price="95$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        psu5 = MagicMock(
            price="150$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        psu6 = MagicMock(
            price="90$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )

        mock_load_psus.return_value = [
            psu1,
            psu2,
            psu3,
            psu4,
            psu5,
            psu6,
        ]

        userBuild = MagicMock()
        userBuild.budget = 1000.0
        userBuild.totalPrice = 1001.0

        result = suggestCompatiblePSUs(userBuild, psuComp=None)

        self.assertEqual(len(result), 5)
        self.assertIn(psu6, result)
        self.assertNotIn(psu5, result)

    @patch("pc_builder.components.psu.loadPSUsfromJSON")
    def test_psu_within_budget(self, mock_load_psus):
        """Testing if psus are filtered correctly within budget"""

        psu1 = MagicMock(
            price="79$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        psu2 = MagicMock(
            price="80$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        psu3 = MagicMock(
            price="81$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )

        mock_load_psus.return_value = [psu1, psu2, psu3]

        userBuild = MagicMock()
        userBuild.budget = 1000.0
        userBuild.totalPrice = 800.0

        result = suggestCompatiblePSUs(userBuild, psuComp=None)

        self.assertEqual(len(result), 2)
        self.assertIn(psu1, result)
        self.assertIn(psu2, result)
        self.assertNotIn(psu3, result)

    @patch("pc_builder.components.psu.loadPSUsfromJSON")
    def test_psu_exceeding_remaining_build_budget(self, mock_load_psus):
        """Testing if psus exceeding remaining total budget are excluded."""

        psu1 = MagicMock(
            price="79$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        psu2 = MagicMock(
            price="80$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        psu3 = MagicMock(
            price="81$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )

        mock_load_psus.return_value = [psu1, psu2, psu3]

        userBuild = MagicMock()
        userBuild.budget = 1000.0
        userBuild.totalPrice = 921.0  # 79 is max price of psu
        userBuild.components = {}

        result = suggestCompatiblePSUs(userBuild, psuComp=None)

        self.assertEqual(len(result), 1)
        self.assertIn(psu1, result)
        self.assertNotIn(psu2, result)
        self.assertNotIn(psu3, result)
