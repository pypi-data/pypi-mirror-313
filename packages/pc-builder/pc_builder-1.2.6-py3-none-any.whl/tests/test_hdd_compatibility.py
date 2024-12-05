import unittest
from unittest.mock import MagicMock
from pc_builder.compatibility.hdd import *


class HDDCompatibility:
    def __init__(self):
        self.compatibilities = {
            "motherboard": {
                "slots": True,
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
        self.components = {"motherboard": [], "case": [], "hdd": [], "ssd": []}


class TestHDDCompatibility(unittest.TestCase):

    def setUp(self):
        # Setup a default HDD with specs for testing
        self.hdd = MagicMock()
        self.hdd.specs.form_factor = ["3.5"]

        # Create a UserBuild instance
        self.userBuild = UserBuild()
        self.hddComp = HDDCompatibility()

    def test_hdd_motherboard_compatible(self):
        """Test HDD and motherboard compatibility (enough SATA ports)"""
        mb = MagicMock()
        mb.specs.sata_ports = ["6"]  # 6 SATA ports available

        self.userBuild.components["motherboard"].append(mb)
        self.userBuild.components["hdd"].append(self.hdd)

        result = checkHDD_MB_CaseCompatibility(self.hdd, self.userBuild, self.hddComp)

        self.assertTrue(result)
        self.assertTrue(self.hddComp.compatibilities["motherboard"]["slots"])

    def test_hdd_with_sata_ssd_motherboard_compatible(self):
        """Test HDD and motherboard compatibility (enough SATA ports)"""
        mb = MagicMock()
        mb.specs.sata_ports = ["3"]  # 3 SATA ports available

        ssd = MagicMock()
        ssd.specs.interface = ["SATA"]

        self.userBuild.components["motherboard"].append(mb)
        self.userBuild.components["hdd"].append(self.hdd)
        self.userBuild.components["ssd"].append(ssd)

        result = checkHDD_MB_CaseCompatibility(self.hdd, self.userBuild, self.hddComp)

        self.assertTrue(result)
        self.assertTrue(self.hddComp.compatibilities["motherboard"]["slots"])

    def test_hdd_with_sata_ssd_motherboard_incompatible(self):
        """Test HDD and motherboard compatibility (enough SATA ports)"""
        mb = MagicMock()
        mb.specs.sata_ports = ["2"]  # 2 SATA ports available

        ssd = MagicMock()
        ssd.specs.interface = ["SATA"]

        self.userBuild.components["motherboard"].append(mb)
        self.userBuild.components["hdd"].append(self.hdd)
        self.userBuild.components["hdd"].append(ssd)

        result = checkHDD_MB_CaseCompatibility(self.hdd, self.userBuild, self.hddComp)

        self.assertFalse(result)
        self.assertFalse(self.hddComp.compatibilities["motherboard"]["slots"])

    def test_hdd_motherboard_incompatible(self):
        """Test HDD and motherboard compatibility (not enough SATA ports)"""
        mb = MagicMock()
        mb.specs.sata_ports = ["1"]  # Only 1 SATA port available

        self.userBuild.components["motherboard"].append(mb)
        self.userBuild.components["hdd"].append(self.hdd)

        result = checkHDD_MB_CaseCompatibility(self.hdd, self.userBuild, self.hddComp)

        self.assertFalse(result)
        self.assertFalse(self.hddComp.compatibilities["motherboard"]["slots"])
        self.assertIn(
            "Incompatible motherboard", self.hddComp.messages["motherboard"][0]
        )

    def test_hdd_case_compatible(self):
        """Test HDD and case compatibility (supported drive bay form factor)"""
        case = MagicMock()
        case.specs.drive_bays = [
            "2 x Internal 3.5",
            "4 x Internal 2.5",
        ]  # Compatible with the HDD form factor

        self.userBuild.components["case"].append(case)
        self.userBuild.components["hdd"].append(self.hdd)

        result = checkHDD_MB_CaseCompatibility(self.hdd, self.userBuild, self.hddComp)

        self.assertTrue(result)
        self.assertTrue(self.hddComp.compatibilities["case"]["drive_bay"])

    def test_hdd_case_incompatible(self):
        """Test HDD and case compatibility (unsupported drive bay form factor)"""
        case = MagicMock()
        case.specs.drive_bays = [
            "2 x Internal 1.5",
            "4 x Internal 2.5",
        ]  # Does not support 3.5" form factor

        self.userBuild.components["case"].append(case)
        self.userBuild.components["hdd"].append(self.hdd)

        result = checkHDD_MB_CaseCompatibility(self.hdd, self.userBuild, self.hddComp)

        self.assertFalse(result)
        self.assertFalse(self.hddComp.compatibilities["case"]["drive_bay"])
        self.assertIn("Incompatible case", self.hddComp.messages["case"][0])

    def test_hdd_compatible_with_both_motherboard_and_case(self):
        """Test HDD compatibility (both motherboard and case are compatible)"""
        mb = MagicMock()
        mb.specs.sata_ports = ["6"]
        case = MagicMock()
        case.specs.drive_bays = [
            "2 x Internal 3.5",
            "4 x Internal 2.5",
        ]

        self.userBuild.components["motherboard"].append(mb)
        self.userBuild.components["case"].append(case)
        self.userBuild.components["hdd"].append(self.hdd)

        result = checkHDD_MB_CaseCompatibility(self.hdd, self.userBuild, self.hddComp)

        self.assertTrue(result)
        self.assertTrue(self.hddComp.compatibilities["motherboard"]["slots"])
        self.assertTrue(self.hddComp.compatibilities["case"]["drive_bay"])

    def test_hdd_incompatible_with_both_motherboard_and_case(self):
        """Test HDD compatibility (both motherboard and case are incompatible)"""
        mb = MagicMock()
        mb.specs.sata_ports = ["1"]  # Only 1 SATA port available
        case = MagicMock()
        case.specs.drive_bays = [
            "2 x Internal 1.5",
            "4 x Internal 2.5",
        ]  # Does not support 3.5" form factor

        self.userBuild.components["motherboard"].append(mb)
        self.userBuild.components["case"].append(case)
        self.userBuild.components["hdd"].append(self.hdd)

        result = checkHDD_MB_CaseCompatibility(self.hdd, self.userBuild, self.hddComp)

        self.assertFalse(result)
        self.assertFalse(self.hddComp.compatibilities["motherboard"]["slots"])
        self.assertFalse(self.hddComp.compatibilities["case"]["drive_bay"])
        self.assertIn(
            "Incompatible motherboard", self.hddComp.messages["motherboard"][0]
        )
        self.assertIn("Incompatible case", self.hddComp.messages["case"][0])


if __name__ == "__main__":
    unittest.main()
