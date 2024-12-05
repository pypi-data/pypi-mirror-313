import unittest
from unittest.mock import MagicMock
from pc_builder.compatibility.ram import *


class RAMCompatibility:
    def __init__(self):
        self.compatibilities = {
            "motherboard": {
                "memory_speed": True,
                "memory_max": True,
                "memory_slots": True,
            },
            "ram": {
                "ddr": True,
            },
        }
        self.messages = {"motherboard": [], "ram": []}


class UserBuild:
    def __init__(self):
        self.components = {"ram": [], "motherboard": []}


class TestRAMCompatibility(unittest.TestCase):
    def setUp(self):
        self.ram = MagicMock()
        self.ram.specs.speed = ["DDR5-5000"]
        self.ram.specs.modules = ["2 x 16GB"]

        self.userBuild = UserBuild()
        self.ramComp = RAMCompatibility()

    def test_singleRam_motherboard_compatible(self):
        motherboard = MagicMock()
        motherboard.specs.memory_speed = ["DDR5-4000", "DDR5-5000", "DDR5-6000"]
        motherboard.specs.memory_max = ["192 GB"]
        motherboard.specs.memory_slots = ["4"]

        self.userBuild.components["motherboard"].append(motherboard)
        result = checkRAM_MotherboardCompatibility(
            self.ram, self.userBuild, self.ramComp
        )

        self.assertTrue(result)
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_speed"])
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_max"])
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_slots"])

    def test_singleRam_motherboard_incompatible_slots(self):
        motherboard = MagicMock()
        motherboard.specs.memory_speed = ["DDR5-4000", "DDR5-5000", "DDR5-6000"]
        motherboard.specs.memory_max = ["192 GB"]
        motherboard.specs.memory_slots = ["1"]

        self.userBuild.components["motherboard"].append(motherboard)
        result = checkRAM_MotherboardCompatibility(
            self.ram, self.userBuild, self.ramComp
        )

        self.assertFalse(result)
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_speed"])
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_max"])
        self.assertFalse(self.ramComp.compatibilities["motherboard"]["memory_slots"])

    def test_singleRam_motherboard_incompatible_capacity(self):
        motherboard = MagicMock()
        motherboard.specs.memory_speed = ["DDR5-4000", "DDR5-5000", "DDR5-6000"]
        motherboard.specs.memory_max = ["16 GB"]
        motherboard.specs.memory_slots = ["2"]

        self.userBuild.components["motherboard"].append(motherboard)
        result = checkRAM_MotherboardCompatibility(
            self.ram, self.userBuild, self.ramComp
        )

        self.assertFalse(result)
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_speed"])
        self.assertFalse(self.ramComp.compatibilities["motherboard"]["memory_max"])
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_slots"])

    def test_singleRam_motherboard_incompatible_speed(self):
        motherboard = MagicMock()
        motherboard.specs.memory_speed = ["DDR4-5000", "DDR5-3000", "DDR5-4000"]
        motherboard.specs.memory_max = ["192 GB"]
        motherboard.specs.memory_slots = ["2"]

        self.userBuild.components["motherboard"].append(motherboard)
        result = checkRAM_MotherboardCompatibility(
            self.ram, self.userBuild, self.ramComp
        )

        self.assertFalse(result)
        self.assertFalse(self.ramComp.compatibilities["motherboard"]["memory_speed"])
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_max"])
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_slots"])

    def test_multipleRam_motherboard_compatible(self):
        motherboard = MagicMock()
        motherboard.specs.memory_speed = ["DDR5-4000", "DDR5-5000", "DDR5-6000"]
        motherboard.specs.memory_max = ["192 GB"]
        motherboard.specs.memory_slots = ["4"]

        ram = MagicMock()
        ram.specs.speed = ["DDR5-6000"]
        ram.specs.modules = ["2 x 8GB"]

        self.userBuild.components["motherboard"].append(motherboard)
        result = checkRAM_MotherboardCompatibility(ram, self.userBuild, self.ramComp)
        self.assertTrue(result)
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_speed"])
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_max"])
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_slots"])

        self.userBuild.components["ram"].append(ram)
        result = checkRAM_MotherboardCompatibility(
            self.ram, self.userBuild, self.ramComp
        )

        self.assertTrue(result)
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_speed"])
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_max"])
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_slots"])

    def test_multipleRam_motherboard_incompatible_slots(self):
        motherboard = MagicMock()
        motherboard.specs.memory_speed = ["DDR5-4000", "DDR5-5000", "DDR5-6000"]
        motherboard.specs.memory_max = ["192 GB"]
        motherboard.specs.memory_slots = ["4"]

        ram = MagicMock()
        ram.specs.speed = ["DDR5-6000"]
        ram.specs.modules = ["3 x 8GB"]

        self.userBuild.components["motherboard"].append(motherboard)
        result = checkRAM_MotherboardCompatibility(ram, self.userBuild, self.ramComp)

        self.assertTrue(result)
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_speed"])
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_max"])
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_slots"])

        self.userBuild.components["ram"].append(ram)
        result = checkRAM_MotherboardCompatibility(
            self.ram, self.userBuild, self.ramComp
        )

        self.assertFalse(result)
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_speed"])
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_max"])
        self.assertFalse(self.ramComp.compatibilities["motherboard"]["memory_slots"])

    def test_multipleRam_motherboard_incompatible_capacity(self):
        motherboard = MagicMock()
        motherboard.specs.memory_speed = ["DDR5-4000", "DDR5-5000", "DDR5-6000"]
        motherboard.specs.memory_max = ["192 GB"]
        motherboard.specs.memory_slots = ["4"]

        ram = MagicMock()
        ram.specs.speed = ["DDR5-6000"]
        ram.specs.modules = ["2 x 81GB"]

        self.userBuild.components["motherboard"].append(motherboard)
        result = checkRAM_MotherboardCompatibility(ram, self.userBuild, self.ramComp)

        self.assertTrue(result)
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_speed"])
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_max"])
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_slots"])

        self.userBuild.components["ram"].append(ram)
        result = checkRAM_MotherboardCompatibility(
            self.ram, self.userBuild, self.ramComp
        )

        self.assertFalse(result)
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_speed"])
        self.assertFalse(self.ramComp.compatibilities["motherboard"]["memory_max"])
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_slots"])

    def test_multipleRam_motherboard_incompatible_speed(self):
        motherboard = MagicMock()
        motherboard.specs.memory_speed = ["DDR5-3000", "DDR5-4000", "DDR5-6000"]
        motherboard.specs.memory_max = ["192 GB"]
        motherboard.specs.memory_slots = ["4"]

        ram = MagicMock()
        ram.specs.speed = ["DDR5-6000"]
        ram.specs.modules = ["2 x 8GB"]

        self.userBuild.components["motherboard"].append(motherboard)
        result = checkRAM_MotherboardCompatibility(ram, self.userBuild, self.ramComp)

        self.assertTrue(result)
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_speed"])
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_max"])
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_slots"])

        self.userBuild.components["ram"].append(ram)
        result = checkRAM_MotherboardCompatibility(
            self.ram, self.userBuild, self.ramComp
        )

        self.assertFalse(result)
        self.assertFalse(self.ramComp.compatibilities["motherboard"]["memory_speed"])
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_max"])
        self.assertTrue(self.ramComp.compatibilities["motherboard"]["memory_slots"])


class TestRAMDDRCompatibility(unittest.TestCase):
    def setUp(self):
        self.userBuild = UserBuild()
        self.ramComp = RAMCompatibility()

    def test_no_existing_ram(self):
        # Case where no RAM is currently in the build
        ram = MagicMock()
        ram.specs.speed = ["DDR4-3200"]

        result = checkMultipleRAMDDRCompatibility(ram, self.userBuild, self.ramComp)
        self.assertTrue(result)
        self.assertTrue(self.ramComp.compatibilities["ram"]["ddr"])

    def test_compatible_ddr_type(self):
        # Case where the new RAM has the same DDR type as existing RAM
        existingRam = MagicMock()
        existingRam.specs.speed = ["DDR4-3200"]

        newRam = MagicMock()
        newRam.specs.speed = ["DDR4-3000"]

        self.userBuild.components["ram"].append(existingRam)

        result = checkMultipleRAMDDRCompatibility(newRam, self.userBuild, self.ramComp)
        self.assertTrue(result)
        self.assertTrue(self.ramComp.compatibilities["ram"]["ddr"])
        self.assertEqual(len(self.ramComp.messages["ram"]), 0)

    def test_incompatible_ddr_type(self):
        # Case where the new RAM has a different DDR type than existing RAM
        existingRam = MagicMock()
        existingRam.specs.speed = ["DDR4-3200"]

        newRam = MagicMock()
        newRam.specs.speed = ["DDR5-4800"]

        self.userBuild.components["ram"].append(existingRam)

        result = checkMultipleRAMDDRCompatibility(newRam, self.userBuild, self.ramComp)
        self.assertFalse(result)
        self.assertFalse(self.ramComp.compatibilities["ram"]["ddr"])
        self.assertIn(
            "Incompatible RAM: The RAM DDR (DDR5) is different from existing RAM'S DDR (DDR4)",
            self.ramComp.messages["ram"],
        )

    def test_multiple_existing_ram_compatible_ddr(self):
        # Case where multiple RAM modules with the same DDR type are present
        existingRam1 = MagicMock()
        existingRam1.specs.speed = ["DDR4-3200"]

        existingRam2 = MagicMock()
        existingRam2.specs.speed = ["DDR4-3000"]

        newRam = MagicMock()
        newRam.specs.speed = ["DDR4-2666"]

        self.userBuild.components["ram"].append(existingRam1)
        self.userBuild.components["ram"].append(existingRam2)

        result = checkMultipleRAMDDRCompatibility(newRam, self.userBuild, self.ramComp)
        self.assertTrue(result)
        self.assertTrue(self.ramComp.compatibilities["ram"]["ddr"])
        self.assertEqual(len(self.ramComp.messages["ram"]), 0)

    def test_multiple_existing_ram_incompatible_ddr(self):
        # Case where there are multiple RAM modules but the new one has a different DDR type
        existingRam1 = MagicMock()
        existingRam1.specs.speed = ["DDR4-3200"]

        existingRam2 = MagicMock()
        existingRam2.specs.speed = ["DDR4-3000"]

        newRam = MagicMock()
        newRam.specs.speed = ["DDR5-4800"]

        self.userBuild.components["ram"].append(existingRam1)
        self.userBuild.components["ram"].append(existingRam2)

        result = checkMultipleRAMDDRCompatibility(newRam, self.userBuild, self.ramComp)
        self.assertFalse(result)
        self.assertFalse(self.ramComp.compatibilities["ram"]["ddr"])
        self.assertIn(
            "Incompatible RAM: The RAM DDR (DDR5) is different from existing RAM'S DDR (DDR4)",
            self.ramComp.messages["ram"],
        )
