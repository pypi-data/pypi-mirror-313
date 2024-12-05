import unittest
from unittest.mock import MagicMock, patch
from pc_builder.suggestions.ssd import suggestCompatibleSSDs


class TestSuggestCompatibleSSDs(unittest.TestCase):

    @patch("pc_builder.components.ssd.loadSSDsfromJSON")
    def test_suggest_compatible_ssds(self, mock_load_ssds):
        """Testing if the function correctly filters out incompatible SSDs."""

        ssd1 = MagicMock()
        ssd1.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
        ssd1.price = "60$"
        ssd1.specs.interface = ["M.2"]

        ssd2 = MagicMock()
        ssd2.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
        ssd2.price = "60$"
        ssd2.specs.interface = ["M.2"]

        ssd3 = MagicMock()
        ssd3.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))
        ssd3.price = "60$"
        ssd3.specs.interface = ["M.2"]

        mock_load_ssds.return_value = [ssd1, ssd2, ssd3]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.useCase = "work"
        userBuild.totalPrice = 700
        userBuild.components = {"ssd": []}
        userBuild.selectedPart.specs.interface = ["M.2 PCIe 4.0 X4"]

        result = suggestCompatibleSSDs(userBuild, ssdComp=None)

        self.assertEqual(len(result), 2)
        self.assertIn(ssd1, result)
        self.assertIn(ssd2, result)
        self.assertNotIn(ssd3, result)

    @patch("pc_builder.components.ssd.loadSSDsfromJSON")
    def test_suggest_compatible_ssds_same_interface(self, mock_load_ssds):
        """Testing if the function correctly filters out incompatible SSDs."""

        ssd1 = MagicMock()
        ssd1.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
        ssd1.price = "60$"
        ssd1.specs.interface = ["M.2"]

        ssd2 = MagicMock()
        ssd2.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
        ssd2.price = "60$"
        ssd2.specs.interface = ["SATA"]

        ssd3 = MagicMock()
        ssd3.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))
        ssd3.price = "60$"
        ssd3.specs.interface = ["M.2"]

        mock_load_ssds.return_value = [ssd1, ssd2, ssd3]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.useCase = "work"
        userBuild.totalPrice = 700
        userBuild.components = {"ssd": []}
        userBuild.selectedPart.specs.interface = ["M.2 PCIe 4.0 X4"]

        result = suggestCompatibleSSDs(userBuild, ssdComp=None)

        self.assertEqual(len(result), 1)
        self.assertIn(ssd1, result)
        self.assertNotIn(ssd2, result)
        self.assertNotIn(ssd3, result)

    @patch("pc_builder.components.ssd.loadSSDsfromJSON")
    def test_suggest_compatible_ssds_same_interface(self, mock_load_ssds):
        """Testing if the function correctly filters out incompatible SSDs."""

        ssd1 = MagicMock()
        ssd1.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
        ssd1.price = "60$"
        ssd1.specs.interface = ["M.2"]

        ssd2 = MagicMock()
        ssd2.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
        ssd2.price = "60$"
        ssd2.specs.interface = ["SATA"]

        ssd3 = MagicMock()
        ssd3.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))
        ssd3.price = "60$"
        ssd3.specs.interface = ["M.2"]

        mock_load_ssds.return_value = [ssd1, ssd2, ssd3]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.useCase = "work"
        userBuild.totalPrice = 700
        userBuild.components = {"ssd": []}
        userBuild.selectedPart.specs.interface = ["SATA"]

        result = suggestCompatibleSSDs(userBuild, ssdComp=None)

        self.assertEqual(len(result), 1)
        self.assertNotIn(ssd1, result)
        self.assertIn(ssd2, result)
        self.assertNotIn(ssd3, result)

    @patch("pc_builder.components.ssd.loadSSDsfromJSON")
    def test_suggest_compatible_ssds_limit_results(self, mock_load_ssds):
        """Testing if the function returns no more than 5 compatible SSDs."""

        compatible_ssds = [MagicMock() for _ in range(10)]
        for ssd in compatible_ssds:
            ssd.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
            ssd.price = "60$"
            ssd.specs.interface = ["M.2"]

        mock_load_ssds.return_value = compatible_ssds

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.useCase = "work"
        userBuild.totalPrice = 700
        userBuild.components = {"ssd": []}
        userBuild.selectedPart.specs.interface = ["M.2"]

        result = suggestCompatibleSSDs(userBuild, ssdComp=None)

        self.assertEqual(len(result), 5)
        for ssd in compatible_ssds[:5]:
            self.assertIn(ssd, result)

    @patch("pc_builder.components.ssd.loadSSDsfromJSON")
    def test_suggest_compatible_ssds_no_compatible_found(self, mock_load_ssds):
        """Testing if the function returns an empty list when no compatible SSDs are found."""

        ssd1 = MagicMock()
        ssd1.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))
        ssd1.price = "60$"
        ssd1.specs.interface = ["M.2"]

        ssd2 = MagicMock()
        ssd2.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))
        ssd2.price = "60$"
        ssd2.specs.interface = ["M.2"]

        mock_load_ssds.return_value = [ssd1, ssd2]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.useCase = "work"
        userBuild.totalPrice = 700
        userBuild.components = {"ssd": []}
        userBuild.selectedPart.specs.interface = ["M.2"]

        result = suggestCompatibleSSDs(userBuild, ssdComp=None)

        self.assertEqual(len(result), 0)


class TestSuggestCompatibleSSDsExtended(unittest.TestCase):

    @patch("pc_builder.components.ssd.loadSSDsfromJSON")
    def test_out_of_budget_returns_cheapest_ssds(self, mock_load_ssds):
        """Testing if out of budget returns only the top 5 cheapest compatible SSDs."""

        ssd1 = MagicMock(
            price="30$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        ssd1.specs.interface = ["M.2"]
        ssd2 = MagicMock(
            price="40$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        ssd2.specs.interface = ["M.2"]
        ssd3 = MagicMock(
            price="50$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        ssd3.specs.interface = ["M.2"]
        ssd4 = MagicMock(
            price="60$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        ssd4.specs.interface = ["M.2"]
        ssd5 = MagicMock(
            price="70$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        ssd5.specs.interface = ["M.2"]
        ssd6 = MagicMock(
            price="80$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        ssd6.specs.interface = ["M.2"]

        mock_load_ssds.return_value = [ssd1, ssd2, ssd3, ssd4, ssd5, ssd6]

        userBuild = MagicMock()
        userBuild.budget = 500
        userBuild.totalPrice = 550  # Budget exceeded
        userBuild.useCase = "gaming"
        userBuild.components = {"ssd": [], "hdd": []}
        userBuild.selectedPart.specs.interface = ["M.2"]

        result = suggestCompatibleSSDs(userBuild, ssdComp=None)

        self.assertEqual(len(result), 5)
        self.assertIn(ssd1, result)
        self.assertNotIn(ssd6, result)

    @patch("pc_builder.components.ssd.loadSSDsfromJSON")
    def test_ssds_within_budget_and_use_case_work(self, mock_load_ssds):
        """Testing if SSDs are filtered correctly within budget and based on use case."""

        ssd1 = MagicMock(
            price="70$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        ssd1.specs.interface = ["M.2"]
        ssd2 = MagicMock(
            price="120$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        ssd2.specs.interface = ["M.2"]
        ssd3 = MagicMock(
            price="130$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        ssd3.specs.interface = ["M.2"]

        mock_load_ssds.return_value = [ssd1, ssd2, ssd3]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.useCase = "work"
        userBuild.totalPrice = 800  # Leaves 200 for components and 120 for SSDs
        userBuild.components = {"ssd": []}
        userBuild.selectedPart.specs.interface = ["M.2"]

        result = suggestCompatibleSSDs(userBuild, ssdComp=None)

        self.assertIn(ssd1, result)  # Within budget
        self.assertIn(ssd2, result)  # Within budget
        self.assertNotIn(ssd3, result)  # Exceeds budget for SSD

    @patch("pc_builder.components.ssd.loadSSDsfromJSON")
    def test_ssds_within_budget_and_use_case_gaming(self, mock_load_ssds):
        """Testing if SSDs are filtered correctly within budget and based on use case."""

        ssd1 = MagicMock(
            price="70$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        ssd1.specs.interface = ["M.2"]
        ssd2 = MagicMock(
            price="100$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        ssd2.specs.interface = ["M.2"]
        ssd3 = MagicMock(
            price="110$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        ssd3.specs.interface = ["M.2"]

        mock_load_ssds.return_value = [ssd1, ssd2, ssd3]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.useCase = "gaming"
        userBuild.totalPrice = 800  # Leaves 200 for components and 100 for SSDs
        userBuild.components = {"ssd": []}
        userBuild.selectedPart.specs.interface = ["M.2"]

        result = suggestCompatibleSSDs(userBuild, ssdComp=None)

        self.assertIn(ssd1, result)  # Within budget
        self.assertIn(ssd2, result)  # Within budget
        self.assertNotIn(ssd3, result)  # Exceeds budget for SSD

    @patch("pc_builder.components.ssd.loadSSDsfromJSON")
    def test_included_existing_ssd_cost(self, mock_load_ssds):
        """Testing if existing SSD cost is factored into remaining SSD budget."""

        existing_ssd = MagicMock(
            price="30$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        existing_ssd.specs.interface = ["M.2"]
        newSSD1 = MagicMock(
            price="30$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        newSSD1.specs.interface = ["M.2"]
        newSSD2 = MagicMock(
            price="31$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        newSSD2.specs.interface = ["M.2"]

        mock_load_ssds.return_value = [newSSD1, newSSD2]

        userBuild = MagicMock()
        userBuild.budget = 500.0
        userBuild.useCase = "work"
        userBuild.totalPrice = 450.0
        userBuild.components = {
            "hdd": [],  # Assuming no SSDs for simplicity
            "ssd": [existing_ssd],  # Already spent $30 on HDD
        }
        userBuild.selectedPart.specs.interface = ["M.2"]

        result = suggestCompatibleSSDs(userBuild, ssdComp=None)

        self.assertEqual(len(result), 1)
        self.assertIn(newSSD1, result)  # Fits in remaining budget
        self.assertNotIn(newSSD2, result)  # Exceeds remaining budget

    @patch("pc_builder.components.ssd.loadSSDsfromJSON")
    def test_included_existing_hdd_and_ssd_cost(self, mock_load_ssds):
        """Testing if existing HDD and SSD costs are factored into remaining budget."""

        existing_hdd = MagicMock(
            price="20$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )

        existing_ssd = MagicMock(
            price="10$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        existing_ssd.specs.interface = ["M.2"]
        newSSD1 = MagicMock(
            price="20$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        newSSD1.specs.interface = ["M.2"]
        newSSD2 = MagicMock(
            price="21$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        newSSD2.specs.interface = ["M.2"]

        mock_load_ssds.return_value = [newSSD1, newSSD2]

        userBuild = MagicMock()
        userBuild.budget = 500.0
        userBuild.useCase = "gaming"
        userBuild.totalPrice = 450.0
        userBuild.components = {
            "hdd": [existing_hdd],
            "ssd": [existing_ssd],
        }  # Already spent $30 on storage
        userBuild.selectedPart.specs.interface = ["M.2"]

        result = suggestCompatibleSSDs(userBuild, ssdComp=None)

        self.assertEqual(len(result), 1)
        self.assertIn(newSSD1, result)  # Fits in remaining budget
        self.assertNotIn(newSSD2, result)  # Exceeds remaining budget
