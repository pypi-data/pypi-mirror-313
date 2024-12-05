import unittest
from unittest.mock import MagicMock
from pc_builder.compatibility.case import *


class CaseCompatibility:
    def __init__(self):
        self.compatibilities = {
            "motherboard": {
                "form_factor": True,
            },
            "gpu": {
                "length": True,
            },
            "hdd": {
                "form_factor": True,
            },
            "ssd": {
                "form_factor": True,
            },
        }
        self.messages = {"motherboard": [], "gpu": [], "hdd": [], "ssd": []}


class UserBuild:
    """A mock class to simulate the user build structure."""

    def __init__(self):
        self.components = {"motherboard": [], "gpu": [], "hdd": [], "ssd": []}


class TestCaseCompatibility(unittest.TestCase):

    def setUp(self):
        # Set up a default case for testing
        self.case = MagicMock()
        self.case.name = "Test Case"
        self.case.specs.motherboard_form_factor = ["ATX", "Micro ATX", "Mini ITX"]
        self.case.specs.max_gpu_length = ["365 mm / 14.37"]
        self.case.specs.drive_bays = ["2 x Internal 3.5", "2 x Internal 2.5"]

        # Create a UserBuild instance
        self.userBuild = UserBuild()
        self.caseComp = CaseCompatibility()

    # Motherboard compatibility tests
    def test_case_motherboard_compatible(self):
        """Test case and motherboard compatibility based on form factor (compatible)"""
        motherboard = MagicMock()
        motherboard.specs.form_factor = ["ATX"]

        self.userBuild.components["motherboard"].append(motherboard)

        result = checkCase_MBCompatibility(self.case, self.userBuild, self.caseComp)

        self.assertTrue(result)
        self.assertTrue(self.caseComp.compatibilities["motherboard"]["form_factor"])

    def test_case_motherboard_incompatible(self):
        """Test case and motherboard compatibility based on form factor (incompatible)"""
        motherboard = MagicMock()
        motherboard.specs.form_factor = ["EATX"]

        self.userBuild.components["motherboard"].append(motherboard)

        result = checkCase_MBCompatibility(self.case, self.userBuild, self.caseComp)

        self.assertFalse(result)
        self.assertFalse(self.caseComp.compatibilities["motherboard"]["form_factor"])
        self.assertIn("Motherboard", self.caseComp.messages["motherboard"][0])

    # GPU compatibility tests
    def test_case_gpu_compatible(self):
        """Test case and GPU compatibility based on length (compatible)"""
        gpu = MagicMock()
        gpu.specs.length = ["300 mm"]

        self.userBuild.components["gpu"].append(gpu)

        result = checkCase_GPUCompatibility(self.case, self.userBuild, self.caseComp)

        self.assertTrue(result)
        self.assertTrue(self.caseComp.compatibilities["gpu"]["length"])

    def test_case_gpu_incompatible(self):
        """Test case and GPU compatibility based on length (incompatible)"""
        gpu = MagicMock()
        gpu.specs.length = ["400 mm"]  # Longer than the case's max length

        self.userBuild.components["gpu"].append(gpu)

        result = checkCase_GPUCompatibility(self.case, self.userBuild, self.caseComp)

        self.assertFalse(result)
        self.assertFalse(self.caseComp.compatibilities["gpu"]["length"])
        self.assertIn("GPU", self.caseComp.messages["gpu"][0])

    # HDD compatibility tests
    def test_case_single_hdd_compatible(self):
        """Test case and a single HDD compatibility based on form factor (compatible)"""
        hdd = MagicMock()
        hdd.name = "Test HDD"
        hdd.specs.form_factor = ["3.5"]

        self.userBuild.components["hdd"].append(hdd)

        result = checkCase_HDDCompatibility(self.case, self.userBuild, self.caseComp)

        self.assertTrue(result)
        self.assertTrue(self.caseComp.compatibilities["hdd"]["form_factor"])

    def test_case_single_hdd_incompatible(self):
        """Test case and a single HDD compatibility based on form factor (incompatible)"""
        hdd = MagicMock()
        hdd.name = "Test HDD"
        hdd.specs.form_factor = ["1.5"]  # No matching drive bay

        self.userBuild.components["hdd"].append(hdd)

        result = checkCase_HDDCompatibility(self.case, self.userBuild, self.caseComp)

        self.assertFalse(result)
        self.assertEqual(
            self.caseComp.compatibilities["hdd"]["form_factor"], [hdd.name]
        )
        self.assertIn("HDDs", self.caseComp.messages["hdd"][0])

    def test_case_multiple_hdd_compatible(self):
        """Test case and multiple HDDs compatibility (all compatible)"""
        hdd1 = MagicMock()
        hdd1.name = "Test 1 HDD"
        hdd1.specs.form_factor = ["3.5"]
        hdd2 = MagicMock()
        hdd2.name = "Test 2 HDD"
        hdd2.specs.form_factor = ["2.5"]

        self.userBuild.components["hdd"].extend([hdd1, hdd2])

        result = checkCase_HDDCompatibility(self.case, self.userBuild, self.caseComp)

        self.assertTrue(result)
        self.assertTrue(self.caseComp.compatibilities["hdd"]["form_factor"])

    def test_case_multiple_hdd_incompatible(self):
        """Test case and multiple HDDs compatibility (one incompatible)"""
        hdd1 = MagicMock()
        hdd1.name = "Test 1 HDD"
        hdd1.specs.form_factor = ["3.5"]
        hdd2 = MagicMock()
        hdd2.name = "Test 2 HDD"
        hdd2.specs.form_factor = ["1.5"]  # No matching drive bay

        self.userBuild.components["hdd"].extend([hdd1, hdd2])

        result = checkCase_HDDCompatibility(self.case, self.userBuild, self.caseComp)

        self.assertFalse(result)
        self.assertEqual(
            self.caseComp.compatibilities["hdd"]["form_factor"], [hdd2.name]
        )
        self.assertIn("HDDs", self.caseComp.messages["hdd"][0])

    # SSD compatibility tests
    def test_case_single_ssd_compatible(self):
        """Test case and a single SSD compatibility based on form factor (compatible)"""
        ssd = MagicMock()
        ssd.name = "Test SSD"
        ssd.specs.form_factor = ["2.5"]
        ssd.specs.interface = ["SATA"]

        self.userBuild.components["ssd"].append(ssd)

        result = checkCase_SSDCompatibility(self.case, self.userBuild, self.caseComp)

        self.assertTrue(result)
        self.assertTrue(self.caseComp.compatibilities["ssd"]["form_factor"])

    def test_case_single_ssd_incompatible(self):
        """Test case and a single SSD compatibility based on form factor (incompatible)"""
        ssd = MagicMock()
        ssd.name = "Test SSD"
        ssd.specs.form_factor = ["1.5"]  # No matching drive bay for this form factor
        ssd.specs.interface = ["SATA"]

        self.userBuild.components["ssd"].append(ssd)

        result = checkCase_SSDCompatibility(self.case, self.userBuild, self.caseComp)

        self.assertFalse(result)
        self.assertEqual(
            self.caseComp.compatibilities["ssd"]["form_factor"], [ssd.name]
        )
        self.assertIn("SSDs", self.caseComp.messages["ssd"][0])

    def test_case_multiple_ssd_compatible(self):
        """Test case and multiple SSDs compatibility (all compatible)"""
        ssd1 = MagicMock()
        ssd1.name = "Test 1 SSD"
        ssd1.specs.form_factor = ["2.5"]
        ssd1.specs.interface = ["SATA"]

        ssd2 = MagicMock()
        ssd2.name = "Test 2 SSD"
        ssd2.specs.form_factor = ["3.5"]
        ssd2.specs.interface = ["SATA"]

        ssd3 = MagicMock()
        ssd3.name = "Test 3 SSD"
        ssd3.specs.form_factor = ["M.2-2280"]
        ssd3.specs.interface = ["M.2 PCIe 4.0 X4"]

        self.userBuild.components["ssd"].extend([ssd1, ssd2, ssd3])

        result = checkCase_SSDCompatibility(self.case, self.userBuild, self.caseComp)

        self.assertTrue(result)
        self.assertTrue(self.caseComp.compatibilities["ssd"]["form_factor"])

    def test_case_multiple_ssd_incompatible(self):
        """Test case and multiple SSDs compatibility (one incompatible)"""
        ssd1 = MagicMock()
        ssd1.name = "Test 1 SSD"
        ssd1.specs.form_factor = ["2.5"]
        ssd1.specs.interface = ["SATA"]

        ssd2 = MagicMock()
        ssd2.name = "Test 2 SSD"
        ssd2.specs.form_factor = ["1.5"]  # No matching drive bay for this form factor
        ssd2.specs.interface = ["SATA"]

        ssd3 = MagicMock()
        ssd3.name = "Test 3 SSD"
        ssd3.specs.form_factor = ["M.2-2280"]
        ssd3.specs.interface = ["M.2 PCIe 4.0 X4"]

        self.userBuild.components["ssd"].extend([ssd1, ssd2, ssd3])

        result = checkCase_SSDCompatibility(self.case, self.userBuild, self.caseComp)

        self.assertFalse(result)
        self.assertEqual(
            self.caseComp.compatibilities["ssd"]["form_factor"], [ssd2.name]
        )
        self.assertIn("SSDs", self.caseComp.messages["ssd"][0])


if __name__ == "__main__":
    unittest.main()
