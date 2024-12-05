import unittest
from unittest.mock import MagicMock, patch
from pc_builder.suggestions.case import suggestCompatibleCases


class TestSuggestCompatibleCases(unittest.TestCase):

    @patch("pc_builder.components.case.loadCasesfromJSON")
    def test_suggest_compatible_cases(self, mock_load_cases):
        """Testing if the function correctly filters out incompatible Cases."""

        case1 = MagicMock()
        case1.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
        case1.price = "50$"

        case2 = MagicMock()
        case2.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
        case2.price = "60$"

        case3 = MagicMock()
        case3.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))
        case3.price = "70$"

        mock_load_cases.return_value = [case1, case2, case3]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.totalPrice = 700
        userBuild.components = {"case": []}

        result = suggestCompatibleCases(userBuild, caseComp=None)

        self.assertEqual(len(result), 1)  # Only one case should be returned
        self.assertIn(
            result[0], [case1]
        )  # The result must be one of the compatible cases
        self.assertNotIn(case3, result)

    @patch("pc_builder.components.case.loadCasesfromJSON")
    def test_suggest_compatible_cases_limit_results(self, mock_load_cases):
        """Testing if the function returns no more than 5 compatible Cases."""

        compatible_cases = [MagicMock() for _ in range(10)]
        for case in compatible_cases:
            case.checkCompatibility = MagicMock(return_value=(True, "Compatible"))
            case.price = "50$"

        mock_load_cases.return_value = compatible_cases

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.totalPrice = 700
        userBuild.components = {"case": []}

        result = suggestCompatibleCases(userBuild, caseComp=None)

        self.assertEqual(len(result), 5)
        for case in compatible_cases[:5]:
            self.assertIn(case, result)

    @patch("pc_builder.components.case.loadCasesfromJSON")
    def test_suggest_compatible_cases_no_compatible_found(self, mock_load_cases):
        """Testing if the function returns an empty list when no compatible Cases are found."""

        case1 = MagicMock()
        case1.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))
        case1.price = "50$"

        case2 = MagicMock()
        case2.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))
        case2.price = "60$"

        mock_load_cases.return_value = [case1, case2]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.totalPrice = 800
        userBuild.components = {"case": []}

        result = suggestCompatibleCases(userBuild, caseComp=None)

        self.assertEqual(len(result), 0)


class TestSuggestCompatibleCasesExtended(unittest.TestCase):

    @patch("pc_builder.components.case.loadCasesfromJSON")
    def test_out_of_budget_returns_cheapest_cases(self, mock_load_cases):
        """Testing if out of budget returns only the top 5 cheapest compatible Cases."""

        case1 = MagicMock(
            price="20$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        case2 = MagicMock(
            price="15$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        case3 = MagicMock(
            price="25$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        case4 = MagicMock(
            price="10$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        case5 = MagicMock(
            price="30$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        case6 = MagicMock(
            price="5$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )

        mock_load_cases.return_value = [case1, case2, case3, case4, case5, case6]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.totalPrice = 1100  # Budget exceeded
        userBuild.components = {"case": []}

        result = suggestCompatibleCases(userBuild, caseComp=None)

        self.assertEqual(len(result), 5)
        self.assertIn(case6, result)
        self.assertNotIn(case5, result)

    @patch("pc_builder.components.case.loadCasesfromJSON")
    def test_cases_within_budget_and_use_case_work(self, mock_load_cases):
        """Testing if Cases are filtered correctly within budget and based on work use case."""

        case1 = MagicMock(
            price="50$", checkCompatibility=MagicMock(return_value=(True, "Compatible"))
        )
        case2 = MagicMock(
            price="120$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )
        case3 = MagicMock(
            price="130$",
            checkCompatibility=MagicMock(return_value=(True, "Compatible")),
        )

        mock_load_cases.return_value = [case1, case2, case3]

        userBuild = MagicMock()
        userBuild.budget = 1000
        userBuild.useCase = "work"
        userBuild.totalPrice = 900  # Leaves 100 for components and 50 for case
        userBuild.components = {"case": []}

        result = suggestCompatibleCases(userBuild, caseComp=None)

        self.assertIn(case1, result)  # Within budget
        self.assertNotIn(case2, result)  # Exceeds budget for case
        self.assertNotIn(case3, result)  # Exceeds budget for case
