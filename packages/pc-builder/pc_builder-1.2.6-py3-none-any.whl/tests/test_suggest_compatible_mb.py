import unittest
from unittest.mock import MagicMock, patch
from pc_builder.suggestions.motherboard import suggestCompatibleMotherboards


class TestSuggestCompatibleMotherboards(unittest.TestCase):

    @patch("pc_builder.components.motherboard.loadMBsfromJSON")
    def test_suggest_compatible_mb(self, mock_load_motherboards):
        """Testing if the function correctly filters out incompatible Motherboards."""

        motherboard1 = MagicMock()
        motherboard1.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
        motherboard1.price = "90$"

        motherboard2 = MagicMock()
        motherboard2.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
        motherboard2.price = "90$"

        motherboard3 = MagicMock()
        motherboard3.checkCompatibility = MagicMock(
            return_value=(False, "Incompatible")
        )
        motherboard3.price = "90$"

        mock_load_motherboards.return_value = [motherboard1, motherboard2, motherboard3]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.totalPrice = 400

        result = suggestCompatibleMotherboards(userBuild, motherboardComp=None)

        self.assertEqual(len(result), 2)
        self.assertIn(motherboard1, result)
        self.assertIn(motherboard2, result)
        self.assertNotIn(motherboard3, result)

    @patch("pc_builder.components.motherboard.loadMBsfromJSON")
    def test_suggest_compatible_mb_limit_results(self, mock_load_motherboards):
        """Testing if the function returns no more than 5 compatible Motherboards."""

        compatible_motherboards = [MagicMock() for _ in range(10)]
        for motherboard in compatible_motherboards:
            motherboard.checkCompatibility = MagicMock(
                return_value=(True, "Compatible")
            )
            motherboard.price = "90$"

        mock_load_motherboards.return_value = compatible_motherboards

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.totalPrice = 400

        result = suggestCompatibleMotherboards(userBuild, motherboardComp=None)

        self.assertEqual(len(result), 5)
        for motherboard in compatible_motherboards[:5]:
            self.assertIn(motherboard, result)

    @patch("pc_builder.components.motherboard.loadMBsfromJSON")
    def test_suggest_compatible_mb_no_compatible_found(self, mock_load_motherboards):
        """Testing if the function returns an empty list when no compatible Motherboards are found."""

        motherboard1 = MagicMock()
        motherboard1.checkCompatibility = MagicMock(
            return_value=(False, "Incompatible")
        )
        motherboard1.price = "90$"

        motherboard2 = MagicMock()
        motherboard2.checkCompatibility = MagicMock(
            return_value=(False, "Incompatible")
        )
        motherboard2.price = "90$"

        mock_load_motherboards.return_value = [motherboard1, motherboard2]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.totalPrice = 400

        result = suggestCompatibleMotherboards(userBuild, motherboardComp=None)

        self.assertEqual(len(result), 0)


class TestSuggestCompatibleMotherboardsExtended(unittest.TestCase):

    @patch("pc_builder.components.motherboard.loadMBsfromJSON")
    def test_out_of_budget_returns_cheapest_mb(self, mock_load_motherboards):
        """Testing if out of budget returns only the top 5 cheapest compatible motherboards."""

        motherboard1 = MagicMock(
            price="85$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        motherboard2 = MagicMock(
            price="80$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        motherboard3 = MagicMock(
            price="100$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        motherboard4 = MagicMock(
            price="95$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        motherboard5 = MagicMock(
            price="150$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        motherboard6 = MagicMock(
            price="90$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )

        mock_load_motherboards.return_value = [
            motherboard1,
            motherboard2,
            motherboard3,
            motherboard4,
            motherboard5,
            motherboard6,
        ]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.totalPrice = 1001
        userBuild.components = {}

        result = suggestCompatibleMotherboards(userBuild, motherboardComp=None)

        self.assertEqual(len(result), 5)
        self.assertIn(motherboard6, result)
        self.assertNotIn(motherboard5, result)

    @patch("pc_builder.components.motherboard.loadMBsfromJSON")
    def test_mb_within_budget(self, mock_load_motherboards):
        """Testing if motherboards are filtered correctly within budget"""

        motherboard1 = MagicMock(
            price="95$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        motherboard2 = MagicMock(
            price="100$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        motherboard3 = MagicMock(
            price="101$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )

        mock_load_motherboards.return_value = [motherboard1, motherboard2, motherboard3]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.totalPrice = 800

        result = suggestCompatibleMotherboards(userBuild, motherboardComp=None)

        self.assertEqual(len(result), 2)
        self.assertIn(motherboard1, result)
        self.assertIn(motherboard2, result)
        self.assertNotIn(motherboard3, result)

    @patch("pc_builder.components.motherboard.loadMBsfromJSON")
    def test_mb_exceeding_remaining_build_budget(self, mock_load_motherboards):
        """Testing if motherboards exceeding remaining total budget are excluded."""

        motherboard1 = MagicMock(
            price="99$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        motherboard2 = MagicMock(
            price="100$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        motherboard3 = MagicMock(
            price="101$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )

        mock_load_motherboards.return_value = [motherboard1, motherboard2, motherboard3]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.totalPrice = 901  # 99 is max price of motherboard
        userBuild.components = {}

        result = suggestCompatibleMotherboards(userBuild, motherboardComp=None)

        self.assertEqual(len(result), 1)
        self.assertIn(motherboard1, result)
        self.assertNotIn(motherboard2, result)
        self.assertNotIn(motherboard3, result)
