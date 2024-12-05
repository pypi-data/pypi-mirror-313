import unittest
from unittest.mock import MagicMock
from pc_builder.compatibility.ssd import *


class SSDCompatibility:
    def __init__(self):
        self.compatibilities = {
            "motherboard": {
                "m2_slots": True,
                "sata_slots": True,
                "interface": True,
            },
            "case": {
                "drive_bay": True,
            },
        }
        self.messages = {
            "motherboard": [],
            "case": [],
        }


class UserBuild:
    """A mock class to simulate the user build structure."""

    def __init__(self):
        self.components = {"motherboard": [], "case": [], "ssd": [], "hdd": []}


class TestSSDCompatibility(unittest.TestCase):

    def setUp(self):
        # Setup a default SSD with specs for testing
        self.ssd = MagicMock()
        self.ssd.specs.form_factor = ["M.2-2280"]
        self.ssd.specs.interface = ["M.2 PCIe 4.0 X4"]

        # Create a UserBuild instance
        self.userBuild = UserBuild()
        self.ssdComp = SSDCompatibility()

    def test_ssd_m2_motherboard_compatible(self):
        """Test SSD and motherboard compatibility (M.2 slot available)"""
        mb = MagicMock()
        mb.specs.m2_slots = ["2260/2280 M-key"]
        self.userBuild.components["motherboard"].append(mb)

        result = checkSSD_MB_CaseCompatibility(self.ssd, self.userBuild, self.ssdComp)

        self.assertTrue(result)
        self.assertTrue(self.ssdComp.compatibilities["motherboard"]["m2_slots"])

    def test_ssd_m2_motherboard_incompatible_slots_full(self):
        """Test SSD and motherboard compatibility (No M.2 slots left)"""
        mb = MagicMock()
        mb.specs.m2_slots = ["2260/2280 M-key"]

        self.userBuild.components["motherboard"].append(mb)
        self.userBuild.components["ssd"].append(self.ssd)

        result = checkSSD_MB_CaseCompatibility(self.ssd, self.userBuild, self.ssdComp)

        self.assertFalse(result)
        self.assertFalse(self.ssdComp.compatibilities["motherboard"]["m2_slots"])
        self.assertIn(
            "Incompatible motherboard", self.ssdComp.messages["motherboard"][0]
        )

    def test_ssd_m2_motherboard_incompatible_form_factor(self):
        """Test SSD and motherboard compatibility (M.2 form factor incompatible)"""
        mb = MagicMock()
        mb.specs.m2_slots = ["2260/2270 M-key"]  # Only supports 2260/2270

        self.userBuild.components["motherboard"].append(mb)

        result = checkSSD_MB_CaseCompatibility(self.ssd, self.userBuild, self.ssdComp)

        self.assertFalse(result)
        self.assertFalse(self.ssdComp.compatibilities["motherboard"]["interface"])
        self.assertIn("Incompatible SSD", self.ssdComp.messages["motherboard"][0])

    def test_ssd_sata_motherboard_compatible(self):
        """Test SSD and motherboard compatibility (SATA slot available)"""
        # Change SSD to SATA interface
        self.ssd.specs.interface = ["SATA 6.0 Gb/s"]
        self.ssd.specs.form_factor = ["2.5"]

        mb = MagicMock()
        mb.specs.sata_ports = ["6"]  # 6 SATA ports available
        self.userBuild.components["motherboard"].append(mb)
        self.userBuild.components["ssd"].append(self.ssd)

        result = checkSSD_MB_CaseCompatibility(self.ssd, self.userBuild, self.ssdComp)

        self.assertTrue(result)
        self.assertTrue(self.ssdComp.compatibilities["motherboard"]["sata_slots"])

    def test_ssd_sata_motherboard_incompatible_ports_full(self):
        """Test SSD and motherboard compatibility (No SATA ports left)"""

        self.ssd.specs.interface = ["SATA 6.0 Gb/s"]
        self.ssd.specs.form_factor = ["2.5"]

        mb = MagicMock()
        mb.specs.sata_ports = ["1"]  # Only 1 SATA port available

        self.userBuild.components["motherboard"].append(mb)

        hdd = MagicMock()
        self.userBuild.components["hdd"].append(hdd)

        result = checkSSD_MB_CaseCompatibility(self.ssd, self.userBuild, self.ssdComp)

        self.assertFalse(result)
        self.assertFalse(self.ssdComp.compatibilities["motherboard"]["sata_slots"])
        self.assertIn(
            "Incompatible motherboard", self.ssdComp.messages["motherboard"][0]
        )

    def test_ssd_case_compatible(self):
        """Test SSD and case compatibility (compatible drive bay)"""

        self.ssd.specs.interface = ["SATA 6.0 Gb/s"]
        self.ssd.specs.form_factor = ["2.5"]

        case = MagicMock()
        case.specs.drive_bays = [
            "2 x Internal 3.5",
            "4 x Internal 2.5",
        ]  # Compatible with the 2.5" SSD

        self.userBuild.components["case"].append(case)

        result = checkSSD_MB_CaseCompatibility(self.ssd, self.userBuild, self.ssdComp)

        self.assertTrue(result)
        self.assertTrue(self.ssdComp.compatibilities["case"]["drive_bay"])

    def test_ssd_case_incompatible(self):
        """Test SSD and case compatibility (incompatible drive bay)"""

        self.ssd.specs.interface = ["SATA 6.0 Gb/s"]
        self.ssd.specs.form_factor = ["2.5"]

        case = MagicMock()
        case.specs.drive_bays = [
            "2 x Internal 3.5",
            "4 x Internal 1.5",
        ]  # Incompatible with the 2.5" SSD

        self.userBuild.components["case"].append(case)

        result = checkSSD_MB_CaseCompatibility(self.ssd, self.userBuild, self.ssdComp)

        self.assertFalse(result)
        self.assertFalse(self.ssdComp.compatibilities["case"]["drive_bay"])
        self.assertIn("Incompatible SSD", self.ssdComp.messages["case"][0])

    def test_ssd_compatible_with_both_motherboard_and_case(self):
        """Test SSD compatibility (both motherboard and case are incompatible)"""
        self.ssd.specs.interface = ["SATA 6.0 Gb/s"]
        self.ssd.specs.form_factor = ["2.5"]

        mb = MagicMock()
        mb.specs.sata_ports = ["2"]
        self.userBuild.components["ssd"].append(self.ssd)

        case = MagicMock()
        case.specs.drive_bays = [
            "2 x Internal 3.5",
            "4 x Internal 2.5",
        ]

        self.userBuild.components["motherboard"].append(mb)
        self.userBuild.components["case"].append(case)

        result = checkSSD_MB_CaseCompatibility(self.ssd, self.userBuild, self.ssdComp)

        self.assertTrue(result)
        self.assertTrue(self.ssdComp.compatibilities["case"]["drive_bay"])
        self.assertTrue(self.ssdComp.compatibilities["motherboard"]["sata_slots"])


if __name__ == "__main__":
    unittest.main()
