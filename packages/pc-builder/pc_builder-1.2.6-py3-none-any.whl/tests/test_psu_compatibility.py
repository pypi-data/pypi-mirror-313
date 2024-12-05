import unittest
from unittest.mock import MagicMock
from pc_builder.compatibility.psu import *


class PSUCompatibility:
    def __init__(self):
        self.compatibilities = {
            "cpu": {
                "tdp": True,
            },
            "gpu": {"tdp": True},
        }
        self.messages = {"cpu": [], "gpu": []}


class UserBuild:
    def __init__(self):
        self.components = {"psu": [], "cpu": [], "gpu": []}


class TestPSUCompatibility(unittest.TestCase):
    def setUp(self):
        self.psu = MagicMock()
        self.psu.specs.wattage = ["500 W"]

        self.userBuild = UserBuild()
        self.psuComp = PSUCompatibility()

    def test_psu_cpu_compatible(self):
        cpu = MagicMock()
        cpu.specs.tdp = ["150 W"]

        self.userBuild.components["cpu"].append(cpu)

        result = checkPSU_CPU_GPUCompatibility(self.psu, self.userBuild, self.psuComp)

        self.assertTrue(result)
        self.assertTrue(self.psuComp.compatibilities["cpu"]["tdp"])

    def test_psu_cpu_incompatible_wattage(self):
        cpu = MagicMock()
        cpu.specs.tdp = ["501 W"]

        self.userBuild.components["cpu"].append(cpu)

        result = checkPSU_CPU_GPUCompatibility(self.psu, self.userBuild, self.psuComp)

        self.assertFalse(result)
        self.assertFalse(self.psuComp.compatibilities["cpu"]["tdp"])

    def test_psu_gpu_compatible(self):
        gpu = MagicMock()
        gpu.specs.tdp = ["150 W"]

        self.userBuild.components["cpu"].append(gpu)

        result = checkPSU_CPU_GPUCompatibility(self.psu, self.userBuild, self.psuComp)

        self.assertTrue(result)
        self.assertTrue(self.psuComp.compatibilities["gpu"]["tdp"])

    def test_psu_gpu_incompatible_wattage(self):
        gpu = MagicMock()
        gpu.specs.tdp = ["501 W"]

        self.userBuild.components["gpu"].append(gpu)

        result = checkPSU_CPU_GPUCompatibility(self.psu, self.userBuild, self.psuComp)

        self.assertFalse(result)
        self.assertFalse(self.psuComp.compatibilities["gpu"]["tdp"])

    def test_psu_cpu_gpu_compatible(self):
        cpu = MagicMock()
        cpu.specs.tdp = ["150 W"]

        gpu = MagicMock()
        gpu.specs.tdp = ["200 W"]

        self.userBuild.components["cpu"].append(cpu)
        self.userBuild.components["gpu"].append(gpu)

        result = checkPSU_CPU_GPUCompatibility(self.psu, self.userBuild, self.psuComp)

        self.assertTrue(result)
        self.assertTrue(self.psuComp.compatibilities["cpu"]["tdp"])
        self.assertTrue(self.psuComp.compatibilities["gpu"]["tdp"])

    def test_psu_cpu_gpu_incompatible_wattage(self):
        cpu = MagicMock()
        cpu.specs.tdp = ["250 W"]

        gpu = MagicMock()
        gpu.specs.tdp = ["251 W"]

        self.userBuild.components["cpu"].append(cpu)
        self.userBuild.components["gpu"].append(gpu)

        self.userBuild.components

        result = checkPSU_CPU_GPUCompatibility(self.psu, self.userBuild, self.psuComp)

        self.assertFalse(result)
        self.assertFalse(self.psuComp.compatibilities["cpu"]["tdp"])
        self.assertFalse(self.psuComp.compatibilities["gpu"]["tdp"])
