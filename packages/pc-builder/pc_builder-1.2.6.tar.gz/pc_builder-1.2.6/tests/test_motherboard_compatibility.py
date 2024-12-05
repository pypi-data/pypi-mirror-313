import unittest
from unittest.mock import MagicMock
from pc_builder.compatibility.motherboard import *

class MotherboardCompatibility:
    def __init__(self):
        self.compatibilities = {
            "ram": {
                "speed": True,
                "slots": True, 
                "capacity": True
            },
            "cpu": {
                "socket_type": True
            },
            "case": {
                "motherboard_form_factor": True
            },
            "ssd": {
                "form_factor": True,
                "slots": True
            },
            "hdd": {
                "ports": True
            }
        }
        self.messages = {"ram": [], "cpu": [], "case": [], "ssd": [], "hdd": []}

class UserBuild:
    def __init__(self):
        self.components = {"motherboard": [], "ram": [], "cpu": [], "case":[], "ssd": [], "hdd": []}

class TestMotherboardCompatibility(unittest.TestCase):
    def setUp(self):
        self.motherboard = MagicMock()
        self.motherboard.specs.memory_speed = ["DDR5-4000", "DDR5-5000", "DDR5-6000"]
        self.motherboard.specs.memory_max = ["192 GB"]
        self.motherboard.specs.memory_slots = ["4"]
        self.motherboard.specs.socket_cpu = ["AM5"]
        self.motherboard.specs.form_factor = ["ATX"]
        self.motherboard.specs.m2_slots = ["2260/2280 M-key"]
        self.motherboard.specs.sata_ports = ["2"]

        self.userBuild = UserBuild()
        self.motherboardComp = MotherboardCompatibility()

    def test_motherboard_singleRam_compatible(self):
        ram = MagicMock()
        ram.specs.speed = ["DDR5-5000"]
        ram.specs.modules = ["2 x 16GB"]

        self.userBuild.components["ram"].append(ram)
        result = checkMotherboard_RAMCompatibility(self.motherboard, self.userBuild, self.motherboardComp)
        
        self.assertTrue(result)
        self.assertTrue(self.motherboardComp.compatibilities["ram"]["speed"])
        self.assertTrue(self.motherboardComp.compatibilities["ram"]["slots"])
        self.assertTrue(self.motherboardComp.compatibilities["ram"]["capacity"])

    def test_motherboard_singleRam_incompatible_slots(self):
        ram = MagicMock()
        ram.specs.speed = ["DDR5-5000"]
        ram.specs.modules = ["5 x 16GB"]

        self.userBuild.components["ram"].append(ram)
        result = checkMotherboard_RAMCompatibility(self.motherboard, self.userBuild, self.motherboardComp)
        
        self.assertFalse(result)
        self.assertTrue(self.motherboardComp.compatibilities["ram"]["speed"])
        self.assertFalse(self.motherboardComp.compatibilities["ram"]["slots"])
        self.assertTrue(self.motherboardComp.compatibilities["ram"]["capacity"])
    
    def test_motherboard_singleRam_incompatible_capacity(self):
        ram = MagicMock()
        ram.specs.speed = ["DDR5-5000"]
        ram.specs.modules = ["2 x 97GB"]

        self.userBuild.components["ram"].append(ram)
        result = checkMotherboard_RAMCompatibility(self.motherboard, self.userBuild, self.motherboardComp)

        self.assertFalse(result)
        self.assertTrue(self.motherboardComp.compatibilities["ram"]["speed"])
        self.assertTrue(self.motherboardComp.compatibilities["ram"]["slots"])
        self.assertFalse(self.motherboardComp.compatibilities["ram"]["capacity"])
    
    def test_motherboard_singleRam_incompatible_speed(self):
        ram = MagicMock()
        ram.name = "RAM"
        ram.specs.speed = ["DDR5-3000"]
        ram.specs.modules = ["2 x 16GB"]

        self.userBuild.components["ram"].append(ram)
        result = checkMotherboard_RAMCompatibility(self.motherboard, self.userBuild, self.motherboardComp)
        incompatibleRAMs = [ram.name]

        self.assertFalse(result)
        self.assertEqual(self.motherboardComp.compatibilities["ram"]["speed"], incompatibleRAMs)
        self.assertTrue(self.motherboardComp.compatibilities["ram"]["slots"])
        self.assertTrue(self.motherboardComp.compatibilities["ram"]["capacity"])

    def test_motherboard_multipleRam_compatible(self):
        ram1 = MagicMock()
        ram1.specs.speed = ["DDR5-5000"]
        ram1.specs.modules = ["2 x 16GB"]

        self.userBuild.components["ram"].append(ram1)

        ram2 = MagicMock()
        ram2.specs.speed = ["DDR5-6000"]
        ram2.specs.modules = ["1 x 8GB"]

        self.userBuild.components["ram"].append(ram2)
        result = checkMotherboard_RAMCompatibility(self.motherboard, self.userBuild, self.motherboardComp)

        print(f"Compatibility check result: {result}")
        print(f"speed compatible: {self.motherboardComp.compatibilities['ram']['speed']}")
        print(f"slots compatible: {self.motherboardComp.compatibilities['ram']['slots']}")
        print(f"capacity compatible: {self.motherboardComp.compatibilities['ram']['capacity']}")
        
        self.assertTrue(result)
        self.assertTrue(self.motherboardComp.compatibilities["ram"]["speed"])
        self.assertTrue(self.motherboardComp.compatibilities["ram"]["slots"])
        self.assertTrue(self.motherboardComp.compatibilities["ram"]["capacity"])

    def test_motherboard_multipleRam_incompatible_slots(self):
        ram1 = MagicMock()
        ram1.specs.speed = ["DDR5-5000"]
        ram1.specs.modules = ["2 x 16GB"]

        self.userBuild.components["ram"].append(ram1)

        ram2 = MagicMock()
        ram2.specs.speed = ["DDR5-6000"]
        ram2.specs.modules = ["3 x 8GB"]

        self.userBuild.components["ram"].append(ram2)
        result = checkMotherboard_RAMCompatibility(self.motherboard, self.userBuild, self.motherboardComp)
        
        self.assertFalse(result)
        self.assertTrue(self.motherboardComp.compatibilities["ram"]["speed"])
        self.assertFalse(self.motherboardComp.compatibilities["ram"]["slots"])
        self.assertTrue(self.motherboardComp.compatibilities["ram"]["capacity"])

    def test_motherboard_multipleRam_incompatible_capacity(self):
        ram1 = MagicMock()
        ram1.specs.speed = ["DDR5-5000"]
        ram1.specs.modules = ["2 x 16GB"]

        self.userBuild.components["ram"].append(ram1)

        ram2 = MagicMock()
        ram2.specs.speed = ["DDR5-6000"]
        ram2.specs.modules = ["1 x 161GB"]

        self.userBuild.components["ram"].append(ram2)
        result = checkMotherboard_RAMCompatibility(self.motherboard, self.userBuild, self.motherboardComp)
        
        self.assertFalse(result)
        self.assertTrue(self.motherboardComp.compatibilities["ram"]["speed"])
        self.assertTrue(self.motherboardComp.compatibilities["ram"]["slots"])
        self.assertFalse(self.motherboardComp.compatibilities["ram"]["capacity"])

    def test_motherboard_multipleRam_incompatible_speed(self):
        ram1 = MagicMock()
        ram1.name = "RAM1"
        ram1.specs.speed = ["DDR5-7000"]
        ram1.specs.modules = ["2 x 16GB"]

        self.userBuild.components["ram"].append(ram1)

        ram2 = MagicMock()
        ram2.name = "RAM2"
        ram2.specs.speed = ["DDR5-2000"]
        ram2.specs.modules = ["1 x 8GB"]

        self.userBuild.components["ram"].append(ram2)
        result = checkMotherboard_RAMCompatibility(self.motherboard, self.userBuild, self.motherboardComp)
        incompatibleRAMs = [ram1.name, ram2.name]
        
        self.assertFalse(result)
        self.assertEqual(self.motherboardComp.compatibilities["ram"]["speed"], incompatibleRAMs)
        self.assertTrue(self.motherboardComp.compatibilities["ram"]["slots"])
        self.assertTrue(self.motherboardComp.compatibilities["ram"]["capacity"])

    def test_motherboard_cpu_compatible(self):
        cpu = MagicMock()
        cpu.specs.socket_type = ["AM5"]

        self.userBuild.components["cpu"].append(cpu)
        result = checkMotherboard_CPUCompatibility(self.motherboard, self.userBuild, self.motherboardComp)
        
        self.assertTrue(result)
        self.assertTrue(self.motherboardComp.compatibilities["cpu"]["socket_type"])

    def test_motherboard_cpu_incompatible_socket(self):
        cpu = MagicMock()
        cpu.specs.socket_type = ["AM6"]

        self.userBuild.components["cpu"].append(cpu)
        result = checkMotherboard_CPUCompatibility(self.motherboard, self.userBuild, self.motherboardComp)

        self.assertFalse(result)
        self.assertFalse(self.motherboardComp.compatibilities["cpu"]["socket_type"])
    
    def test_motherboard_case_compatible(self):
        case = MagicMock()
        case.specs.motherboard_form_factor = ["Micro ATX", "ATX"]

        self.userBuild.components["case"].append(case)
        result = checkMotherboard_CaseCompatibility(self.motherboard, self.userBuild, self.motherboardComp)
        
        self.assertTrue(result)
        self.assertTrue(self.motherboardComp.compatibilities["case"]["motherboard_form_factor"])

    def test_motherboard_case_compatible_multipleformfactors(self):
        case = MagicMock()
        case.specs.motherboard_form_factor = ["Micro ATX", "ATX", "Mini ITX"]
        self.userBuild.components["case"].append(case)

        result = checkMotherboard_CaseCompatibility(self.motherboard, self.userBuild, self.motherboardComp)
        self.assertTrue(result)
        self.assertTrue(self.motherboardComp.compatibilities["case"]["motherboard_form_factor"])

    def test_motherboard_case_incompatible_form(self):
        case = MagicMock()
        case.specs.motherboard_form_factor = ["ETX", "Micro ATX"]

        self.userBuild.components["case"].append(case)
        result = checkMotherboard_CaseCompatibility(self.motherboard, self.userBuild, self.motherboardComp)

        self.assertFalse(result)
        self.assertFalse(self.motherboardComp.compatibilities["case"]["motherboard_form_factor"])
    
    def test_motherboard_ssd_hdd_compatible(self):
        ssdM2 = MagicMock()
        ssdM2.specs.interface = ["M.2 PCIe 4.0 X4"]
        ssdM2.specs.form_factor = ["M.2-2280"]

        self.userBuild.components["ssd"].append(ssdM2)

        ssdSATA = MagicMock()
        ssdSATA.specs.interface = ["SATA 6.0 Gb/s"]
        ssdSATA.specs.form_factor = ["2.5"]

        self.userBuild.components["ssd"].append(ssdSATA)

        hdd = MagicMock()

        self.userBuild.components["hdd"].append(hdd)

        result = checkMotherboard_SSD_HDDCompatibility(self.motherboard, self.userBuild, self.motherboardComp)

        self.assertTrue(result)
        self.assertTrue(self.motherboardComp.compatibilities["ssd"]["form_factor"])
        self.assertTrue(self.motherboardComp.compatibilities["ssd"]["slots"])
        self.assertTrue(self.motherboardComp.compatibilities["hdd"]["ports"])

    def test_motherboard_ssd_hdd_incompatible_m2slots(self):
        ssdM21 = MagicMock()
        ssdM21.specs.interface = ["M.2 PCIe 4.0 X4"]
        ssdM21.specs.form_factor = ["M.2-2280"]

        self.userBuild.components["ssd"].append(ssdM21)

        ssdM22 = MagicMock()
        ssdM22.specs.interface = ["M.2 PCIe 4.0 X4"]
        ssdM22.specs.form_factor = ["M.2-2280"]

        self.userBuild.components["ssd"].append(ssdM22)

        ssdSATA = MagicMock()
        ssdSATA.specs.interface = ["SATA 6.0 Gb/s"]
        ssdSATA.specs.form_factor = ["2.5"]

        self.userBuild.components["ssd"].append(ssdSATA)

        hdd = MagicMock()

        self.userBuild.components["hdd"].append(hdd)

        result = checkMotherboard_SSD_HDDCompatibility(self.motherboard, self.userBuild, self.motherboardComp)

        self.assertFalse(result)
        self.assertTrue(self.motherboardComp.compatibilities["ssd"]["form_factor"])
        self.assertFalse(self.motherboardComp.compatibilities["ssd"]["slots"])
        self.assertTrue(self.motherboardComp.compatibilities["hdd"]["ports"])

    def test_motherboard_ssd_hdd_incompatible_m2formfactor(self):
        ssdM2 = MagicMock()
        ssdM2.name = "M.2 SSD"
        ssdM2.specs.interface = ["M.2 PCIe 4.0 X4"]
        ssdM2.specs.form_factor = ["M.2-22801"]

        self.userBuild.components["ssd"].append(ssdM2)

        ssdSATA = MagicMock()
        ssdSATA.specs.interface = ["SATA 6.0 Gb/s"]
        ssdSATA.specs.form_factor = ["2.5"]

        self.userBuild.components["ssd"].append(ssdSATA)

        hdd = MagicMock()

        self.userBuild.components["hdd"].append(hdd)

        result = checkMotherboard_SSD_HDDCompatibility(self.motherboard, self.userBuild, self.motherboardComp)
        incompatibleSSD = [ssdM2.name]

        self.assertFalse(result)
        self.assertEqual(self.motherboardComp.compatibilities["ssd"]["form_factor"], incompatibleSSD)
        self.assertTrue(self.motherboardComp.compatibilities["ssd"]["slots"])
        self.assertTrue(self.motherboardComp.compatibilities["hdd"]["ports"])

    def test_motherboard_ssd_hdd_incompatible_sataports(self):
        ssdM2 = MagicMock()
        ssdM2.specs.interface = ["M.2 PCIe 4.0 X4"]
        ssdM2.specs.form_factor = ["M.2-2280"]

        self.userBuild.components["ssd"].append(ssdM2)

        ssdSATA = MagicMock()
        ssdSATA.specs.interface = ["SATA 6.0 Gb/s"]
        ssdSATA.specs.form_factor = ["2.5"]

        self.userBuild.components["ssd"].append(ssdSATA)

        hdd1 = MagicMock()
        hdd2 = MagicMock()

        self.userBuild.components["hdd"].append(hdd1)
        self.userBuild.components["hdd"].append(hdd2)

        result = checkMotherboard_SSD_HDDCompatibility(self.motherboard, self.userBuild, self.motherboardComp)

        self.assertFalse(result)
        self.assertTrue(self.motherboardComp.compatibilities["ssd"]["form_factor"])
        self.assertTrue(self.motherboardComp.compatibilities["ssd"]["slots"])
        self.assertFalse(self.motherboardComp.compatibilities["hdd"]["ports"])