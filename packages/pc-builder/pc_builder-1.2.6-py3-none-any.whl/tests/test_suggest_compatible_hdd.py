import unittest
from unittest.mock import MagicMock, patch
from pc_builder.suggestions.hdd import suggestCompatibleHDDs


class TestSuggestCompatibleHDDs(unittest.TestCase):

    @patch("pc_builder.components.hdd.loadHDDsfromJSON")
    def test_suggest_compatible_hdds(self, mock_load_hdds):
        """Testing if the function correctly filters out incompatible HDDs."""

        hdd1 = MagicMock()
        hdd1.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
        hdd1.price = "50$"

        hdd2 = MagicMock()
        hdd2.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
        hdd2.price = "50$"

        hdd3 = MagicMock()
        hdd3.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))
        hdd3.price = "50$"

        mock_load_hdds.return_value = [hdd1, hdd2, hdd3]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.useCase = "work"
        userBuild.totalPrice = 700
        userBuild.components = {"hdd": []}

        result = suggestCompatibleHDDs(userBuild, hddComp=None)

        self.assertEqual(len(result), 2)
        self.assertIn(hdd1, result)
        self.assertIn(hdd2, result)
        self.assertNotIn(hdd3, result)

    @patch("pc_builder.components.hdd.loadHDDsfromJSON")
    def test_suggest_compatible_hdds_limit_results(self, mock_load_hdds):
        """Testing if the function returns no more than 5 compatible HDDs."""

        compatible_hdds = [MagicMock() for _ in range(10)]
        for hdd in compatible_hdds:
            hdd.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
            hdd.price = "50$"

        mock_load_hdds.return_value = compatible_hdds

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.useCase = "work"
        userBuild.totalPrice = 700
        userBuild.components = {"hdd": []}

        result = suggestCompatibleHDDs(userBuild, hddComp=None)

        self.assertEqual(len(result), 5)
        for hdd in compatible_hdds[:5]:
            self.assertIn(hdd, result)

    @patch("pc_builder.components.hdd.loadHDDsfromJSON")
    def test_suggest_compatible_hdds_no_compatible_found(self, mock_load_hdds):
        """Testing if the function returns an empty list when no compatible HDDs are found."""

        hdd1 = MagicMock()
        hdd1.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))
        hdd1.price = "50$"

        hdd2 = MagicMock()
        hdd2.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))
        hdd2.price = "50$"

        mock_load_hdds.return_value = [hdd1, hdd2]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.useCase = "work"
        userBuild.totalPrice = 700
        userBuild.components = {"hdd": []}

        result = suggestCompatibleHDDs(userBuild, hddComp=None)

        self.assertEqual(len(result), 0)


class TestSuggestCompatibleHDDsExtended(unittest.TestCase):

    @patch("pc_builder.components.hdd.loadHDDsfromJSON")
    def test_out_of_budget_returns_cheapest_hdds(self, mock_load_hdds):
        """Testing if out of budget returns only the top 5 cheapest compatible HDDs."""

        hdd1 = MagicMock(
            price="20$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        hdd2 = MagicMock(
            price="15$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        hdd3 = MagicMock(
            price="25$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        hdd4 = MagicMock(
            price="10$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        hdd5 = MagicMock(
            price="30$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        hdd6 = MagicMock(
            price="5$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )

        mock_load_hdds.return_value = [hdd1, hdd2, hdd3, hdd4, hdd5, hdd6]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.totalPrice = 1100  # Budget exceeded
        userBuild.useCase = "gaming"
        userBuild.components = {"hdd": [], "ssd": []}

        result = suggestCompatibleHDDs(userBuild, hddComp=None)

        self.assertEqual(len(result), 5)
        self.assertIn(hdd6, result)
        self.assertNotIn(hdd5, result)

    @patch("pc_builder.components.hdd.loadHDDsfromJSON")
    def test_hdds_within_budget_and_use_case_work(self, mock_load_hdds):
        """Testing if HDDs are filtered correctly within budget and based on use case."""

        hdd1 = MagicMock(
            price="50$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        hdd2 = MagicMock(
            price="120$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        hdd3 = MagicMock(
            price="130$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )

        mock_load_hdds.return_value = [hdd1, hdd2, hdd3]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.useCase = "work"
        userBuild.totalPrice = 700  # Leaves 300 for components and 120 for HDDs
        userBuild.components = {"hdd": [], "ssd": []}

        result = suggestCompatibleHDDs(userBuild, hddComp=None)

        self.assertIn(hdd1, result)  # Within budget
        self.assertIn(hdd2, result)  # Within budget
        self.assertNotIn(hdd3, result)  # Exceeds budget for HDD

    @patch("pc_builder.components.hdd.loadHDDsfromJSON")
    def test_hdds_within_budget_and_use_case_gaming(self, mock_load_hdds):
        """Testing if HDDs are filtered correctly within budget and based on gaming use case."""

        hdd1 = MagicMock(
            price="80$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        hdd2 = MagicMock(
            price="100$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        hdd3 = MagicMock(
            price="120$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )

        mock_load_hdds.return_value = [hdd1, hdd2, hdd3]

        userBuild = MagicMock()
        userBuild.budget = 1000.0
        userBuild.useCase = "gaming"
        userBuild.totalPrice = 700.0  # Leaves 300 for components and 100 for HDDs
        userBuild.components = {"hdd": [], "ssd": []}

        result = suggestCompatibleHDDs(userBuild, hddComp=None)

        self.assertIn(hdd1, result)  # Within budget
        self.assertIn(hdd2, result)  # Within budget
        self.assertNotIn(hdd3, result)  # Exceeds budget for HDD

    @patch("pc_builder.components.hdd.loadHDDsfromJSON")
    def test_included_existing_hdd_cost(self, mock_load_hdds):
        """Testing if existing HDD cost is factored into remaining HDD budget."""

        existing_hdd = MagicMock(
            price="30$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        newHDD1 = MagicMock(
            price="20$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        newHDD2 = MagicMock(
            price="21$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )

        mock_load_hdds.return_value = [newHDD1, newHDD2]

        userBuild = MagicMock()
        userBuild.budget = 500.0
        userBuild.useCase = "gaming"
        userBuild.totalPrice = 450.0
        userBuild.components = {
            "hdd": [existing_hdd],  # Already spent $30 on HDD
            "ssd": [],  # Assuming no SSDs for simplicity
        }

        result = suggestCompatibleHDDs(userBuild, hddComp=None)

        self.assertEqual(len(result), 1)
        self.assertIn(newHDD1, result)  # Fits in remaining budget
        self.assertNotIn(newHDD2, result)  # Exceeds remaining budget

    @patch("pc_builder.components.hdd.loadHDDsfromJSON")
    def test_included_existing_hdd_and_ssd_cost(self, mock_load_hdds):
        """Testing if existing HDD and SSD costs are factored into remaining budget."""

        existing_hdd = MagicMock(
            price="10$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        existing_ssd = MagicMock(
            price="20$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        newHDD1 = MagicMock(
            price="30$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        newHDD2 = MagicMock(
            price="31$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )

        mock_load_hdds.return_value = [newHDD1, newHDD2]

        userBuild = MagicMock()
        userBuild.budget = 500.0
        userBuild.useCase = "work"
        userBuild.totalPrice = 450.0
        userBuild.components = {
            "hdd": [existing_hdd],
            "ssd": [existing_ssd],
        }  # Already spent $30 on storage

        result = suggestCompatibleHDDs(userBuild, hddComp=None)

        self.assertEqual(len(result), 1)
        self.assertIn(newHDD1, result)  # Fits in remaining budget
        self.assertNotIn(newHDD2, result)  # Exceeds remaining budget
