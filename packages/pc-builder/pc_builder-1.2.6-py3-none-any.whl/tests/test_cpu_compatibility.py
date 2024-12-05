import unittest
from unittest.mock import MagicMock
from pc_builder.compatibility.cpu import *


class CPUCompatibility:
    def __init__(self):
        self.compatibilities = {
            "motherboard": {"socket_cpu": True},
            "cpucooler": {"cpu_sockets": True},
            "psu": {"wattage": True},
        }
        self.messages = {"motherboard": [], "cpucooler": [], "psu": []}


class UserBuild:
    """A mock class to simulate the user build structure."""

    def __init__(self):
        self.components = {"motherboard": [], "cpucooler": [], "psu": [], "gpu": []}


class TestCPUCompatibility(unittest.TestCase):

    def setUp(self):
        # Set up a default CPU for testing
        self.cpu = MagicMock()
        self.cpu.specs.socket_type = ["LGA1151"]
        self.cpu.specs.tdp = ["65 W"]

        # Create a UserBuild instance
        self.userBuild = UserBuild()
        self.cpuComp = CPUCompatibility()

    # Motherboard compatibility tests
    def test_cpu_motherboard_compatible(self):
        """Test CPU and motherboard compatibility based on socket type (compatible)"""
        motherboard = MagicMock()
        motherboard.specs.socket_cpu = ["LGA1151"]  # Compatible socket type

        self.userBuild.components["motherboard"].append(motherboard)

        result = checkCPU_MotherboardCompatibility(
            self.cpu, self.userBuild, self.cpuComp
        )

        self.assertTrue(result)
        self.assertTrue(self.cpuComp.compatibilities["motherboard"]["socket_cpu"])

    def test_cpu_motherboard_incompatible(self):
        """Test CPU and motherboard compatibility based on socket type (incompatible)"""
        motherboard = MagicMock()
        motherboard.specs.socket_cpu = ["AM4"]  # Incompatible socket type

        self.userBuild.components["motherboard"].append(motherboard)

        result = checkCPU_MotherboardCompatibility(
            self.cpu, self.userBuild, self.cpuComp
        )

        self.assertFalse(result)
        self.assertFalse(self.cpuComp.compatibilities["motherboard"]["socket_cpu"])
        self.assertIn(
            "Incompatible CPU socket", self.cpuComp.messages["motherboard"][0]
        )

    # CPU Cooler compatibility tests
    def test_cpu_cooler_compatible(self):
        """Test CPU and cooler compatibility based on socket type (compatible)"""
        cpuCooler = MagicMock()
        cpuCooler.specs.cpu_sockets = ["LGA1151"]  # Compatible cooler socket

        self.userBuild.components["cpucooler"].append(cpuCooler)

        result = checkCPU_CPUCoolerCompatibility(self.cpu, self.userBuild, self.cpuComp)

        self.assertTrue(result)
        self.assertTrue(self.cpuComp.compatibilities["cpucooler"]["cpu_sockets"])

    def test_cpu_cooler_incompatible(self):
        """Test CPU and cooler compatibility based on socket type (incompatible)"""
        cpuCooler = MagicMock()
        cpuCooler.specs.cpu_sockets = ["AM4"]  # Incompatible cooler socket

        self.userBuild.components["cpucooler"].append(cpuCooler)

        result = checkCPU_CPUCoolerCompatibility(self.cpu, self.userBuild, self.cpuComp)

        self.assertFalse(result)
        self.assertFalse(self.cpuComp.compatibilities["cpucooler"]["cpu_sockets"])
        self.assertIn("Incompatible CPU cooler", self.cpuComp.messages["cpucooler"][0])

    # PSU compatibility tests
    def test_cpu_psu_compatible(self):
        """Test CPU and PSU compatibility based on wattage (compatible)"""
        psu = MagicMock()
        psu.specs.wattage = ["500 W"]  # Sufficient PSU wattage

        self.userBuild.components["psu"].append(psu)

        result = checkCPU_PSUCompatibility(self.cpu, self.userBuild, self.cpuComp)

        self.assertTrue(result)
        self.assertTrue(self.cpuComp.compatibilities["psu"]["wattage"])

    def test_cpu_psu_incompatible(self):
        """Test CPU and PSU compatibility based on wattage (incompatible)"""
        psu = MagicMock()
        psu.specs.wattage = ["50 W"]  # Insufficient PSU wattage

        self.userBuild.components["psu"].append(psu)

        result = checkCPU_PSUCompatibility(self.cpu, self.userBuild, self.cpuComp)

        self.assertFalse(result)
        self.assertFalse(self.cpuComp.compatibilities["psu"]["wattage"])
        self.assertIn("Incompatible PSU wattage", self.cpuComp.messages["psu"][0])

    def test_cpu_psu_with_gpu_compatible(self):
        """Test CPU and PSU compatibility with a GPU included (compatible)"""
        psu = MagicMock()
        psu.specs.wattage = ["600 W"]  # Sufficient wattage for CPU + GPU

        gpu = MagicMock()
        gpu.specs.tdp = ["150 W"]

        self.userBuild.components["psu"].append(psu)
        self.userBuild.components["gpu"].append(gpu)

        result = checkCPU_PSUCompatibility(self.cpu, self.userBuild, self.cpuComp)

        self.assertTrue(result)
        self.assertTrue(self.cpuComp.compatibilities["psu"]["wattage"])

    def test_cpu_psu_with_gpu_incompatible(self):
        """Test CPU and PSU compatibility with a GPU included (incompatible)"""
        psu = MagicMock()
        psu.specs.wattage = ["200 W"]  # Insufficient wattage for CPU + GPU

        gpu = MagicMock()
        gpu.specs.tdp = ["150 W"]

        self.userBuild.components["psu"].append(psu)
        self.userBuild.components["gpu"].append(gpu)

        result = checkCPU_PSUCompatibility(self.cpu, self.userBuild, self.cpuComp)

        self.assertFalse(result)
        self.assertFalse(self.cpuComp.compatibilities["psu"]["wattage"])
        self.assertIn("Incompatible PSU wattage", self.cpuComp.messages["psu"][0])


if __name__ == "__main__":
    unittest.main()
