import unittest
from unittest.mock import MagicMock
from pc_builder.compatibility.cpucooler import *


class CPUCoolerCompatibility:
    def __init__(self):
        self.compatibilities = {
            "cpu": {
                "socket": True,
            },
        }
        # Change to a dictionary for holding messages
        self.messages = {"cpu": []}


class UserBuild:
    """A mock class to simulate the user build structure."""

    def __init__(self):
        self.components = {"cpu": [], "cpucooler": []}


class TestCPUCoolerCompatibility(unittest.TestCase):

    def setUp(self):
        # Setup a default CPU cooler for testing
        self.cpuCooler = MagicMock()
        self.cpuCooler.specs.cpu_sockets = ["AM4"]

        # Create a UserBuild instance
        self.userBuild = UserBuild()
        self.cpuCoolerComp = CPUCoolerCompatibility()

    def test_cpu_cooler_compatible(self):
        """Test CPU cooler and CPU compatibility based on socket type (compatible)"""
        cpu = MagicMock()
        cpu.specs.socket_type = ["AM4"]  # Compatible socket type

        self.userBuild.components["cpu"].append(cpu)

        result = checkCPUCooler_CPUCompatibility(
            self.cpuCooler, self.userBuild, self.cpuCoolerComp
        )

        self.assertTrue(result)
        self.assertTrue(self.cpuCoolerComp.compatibilities["cpu"]["socket"])

    def test_cpu_cooler_incompatible(self):
        """Test CPU cooler and CPU compatibility based on socket type (incompatible)"""
        cpu = MagicMock()
        cpu.specs.socket_type = ["TR4"]  # Incompatible socket type

        self.userBuild.components["cpu"].append(cpu)

        result = checkCPUCooler_CPUCompatibility(
            self.cpuCooler, self.userBuild, self.cpuCoolerComp
        )

        self.assertFalse(result)
        self.assertFalse(self.cpuCoolerComp.compatibilities["cpu"]["socket"])
        self.assertIn("Incompatible CPU cooler", self.cpuCoolerComp.messages["cpu"][0])

    def test_cpu_cooler_with_no_cpu(self):
        """Test CPU cooler compatibility when no CPU is present"""
        result = checkCPUCooler_CPUCompatibility(
            self.cpuCooler, self.userBuild, self.cpuCoolerComp
        )

        self.assertTrue(result)
        self.assertTrue(self.cpuCoolerComp.compatibilities["cpu"]["socket"])


if __name__ == "__main__":
    unittest.main()
