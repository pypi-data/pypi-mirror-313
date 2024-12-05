import unittest
from unittest.mock import MagicMock
from pc_builder.compatibility.gpu import *


class GPUCompatibility:
    def __init__(self):
        self.compatibilities = {
            "psu": {
                "wattage": True,
            },
            "case": {
                "length": True,
            },
        }
        # Change to a dictionary
        self.messages = {"psu": [], "case": []}


class UserBuild:
    """A mock class to simulate the user build structure."""

    def __init__(self):
        self.components = {"cpu": [], "gpu": [], "psu": [], "case": []}


class TestGPUCompatibility(unittest.TestCase):

    def setUp(self):
        # Setup a default GPU with specs for testing
        self.gpu = MagicMock()
        self.gpu.specs.tdp = ["200 W"]
        self.gpu.specs.length = ["300 mm"]

        # Create a UserBuild instance
        self.userBuild = UserBuild()
        self.gpuComp = GPUCompatibility()

    def test_gpu_psu_compatible(self):
        """Test GPU and PSU compatibility based on wattage (compatible)"""
        psu = MagicMock()
        psu.specs.wattage = ["500 W"]

        self.userBuild.components["psu"].append(psu)

        result = checkGPU_PSUCompatibility(self.gpu, self.userBuild, self.gpuComp)

        self.assertTrue(result)
        self.assertTrue(self.gpuComp.compatibilities["psu"]["wattage"])

    def test_gpu_psu_incompatible(self):
        """Test GPU and PSU compatibility based on wattage (incompatible)"""
        psu = MagicMock()
        psu.specs.wattage = ["150 W"]

        self.userBuild.components["psu"].append(psu)

        result = checkGPU_PSUCompatibility(self.gpu, self.userBuild, self.gpuComp)

        self.assertFalse(result)
        self.assertFalse(self.gpuComp.compatibilities["psu"]["wattage"])

    def test_gpu_psu_with_cpu_compatible(self):
        """Test GPU, CPU, and PSU compatibility based on combined wattage (compatible)"""
        psu = MagicMock()
        psu.specs.wattage = ["600 W"]
        cpu = MagicMock()
        cpu.specs.tdp = ["200 W"]

        self.userBuild.components["psu"].append(psu)
        self.userBuild.components["cpu"].append(cpu)

        result = checkGPU_PSUCompatibility(self.gpu, self.userBuild, self.gpuComp)

        self.assertTrue(result)
        self.assertTrue(self.gpuComp.compatibilities["psu"]["wattage"])

    def test_gpu_psu_with_cpu_incompatible(self):
        """Test GPU, CPU, and PSU compatibility based on combined wattage (incompatible)"""
        psu = MagicMock()
        psu.specs.wattage = ["300 W"]
        cpu = MagicMock()
        cpu.specs.tdp = ["200 W"]

        self.userBuild.components["psu"].append(psu)
        self.userBuild.components["cpu"].append(cpu)

        result = checkGPU_PSUCompatibility(self.gpu, self.userBuild, self.gpuComp)

        self.assertFalse(result)
        self.assertFalse(self.gpuComp.compatibilities["psu"]["wattage"])

    def test_gpu_case_compatible(self):
        """Test GPU and case compatibility based on GPU length (compatible)"""
        case = MagicMock()
        case.specs.max_gpu_length = ["350 mm"]

        self.userBuild.components["case"].append(case)

        result = checkGPU_CaseCompatibility(self.gpu, self.userBuild, self.gpuComp)

        self.assertTrue(result)
        self.assertTrue(self.gpuComp.compatibilities["case"]["length"])

    def test_gpu_case_incompatible(self):
        """Test GPU and case compatibility based on GPU length (incompatible)"""
        case = MagicMock()
        case.specs.max_gpu_length = ["250 mm"]

        self.userBuild.components["case"].append(case)

        result = checkGPU_CaseCompatibility(self.gpu, self.userBuild, self.gpuComp)

        self.assertFalse(result)
        self.assertFalse(self.gpuComp.compatibilities["case"]["length"])


if __name__ == "__main__":
    unittest.main()
