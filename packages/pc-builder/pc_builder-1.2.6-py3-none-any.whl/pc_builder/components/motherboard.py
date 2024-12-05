import time
import json
from pypartpicker import Scraper
from pc_builder.compatibility.motherboard import *


class MotherboardCompatibility:
    def __init__(self):
        self.compatibilities = {
            "ram": {"speed": True, "slots": True, "capacity": True},
            "cpu": {"socket_type": True},
            "case": {"motherboard_form_factor": True},
            "ssd": {"form_factor": True, "slots": True},
            "hdd": {"ports": True},
        }
        self.messages = {"ram": [], "cpu": [], "case": [], "ssd": [], "hdd": []}


class MotherboardSpecs:
    def __init__(
        self,
        manufacturer,
        model,
        part_number,
        socket_cpu,
        chipset,
        form_factor,
        memory_type,
        memory_speed,
        memory_max,
        memory_slots,
        pcie_slots,
        m2_slots,
        sata_ports,
        usb_ports,
        wireless,
        ethernet,
    ):
        self.manufacturer = manufacturer
        self.model = model
        self.part_number = part_number
        self.socket_cpu = socket_cpu
        self.chipset = chipset
        self.form_factor = form_factor
        self.memory_type = memory_type
        self.memory_speed = memory_speed
        self.memory_max = memory_max
        self.memory_slots = memory_slots
        self.pcie_slots = pcie_slots
        self.m2_slots = m2_slots
        self.sata_ports = sata_ports
        self.usb_ports = usb_ports
        self.wireless = wireless
        self.ethernet = ethernet

    def to_dict(self):
        return self.__dict__


class Motherboard:
    def __init__(self, url, name, price, mb_specs):
        self.url = url
        self.name = name
        self.price = price
        self.specs = mb_specs  # Pass the MotherboardSpecs object directly

    def to_dict(self):
        return {
            "url": self.url,
            "name": self.name,
            "price": self.price,
            "specs": self.specs.to_dict(),
        }

    def checkCompatibility(self, userBuild):
        motherboardComp = MotherboardCompatibility()
        isCompatible = True

        if not checkMotherboard_RAMCompatibility(self, userBuild, motherboardComp):
            isCompatible = False

        if not checkMotherboard_CPUCompatibility(self, userBuild, motherboardComp):
            isCompatible = False

        if not checkMotherboard_CaseCompatibility(self, userBuild, motherboardComp):
            isCompatible = False

        if not checkMotherboard_SSD_HDDCompatibility(self, userBuild, motherboardComp):
            isCompatible = False

        return isCompatible, motherboardComp


def saveMBsToJSON(pcpp: Scraper, num_of_parts: int):
    parts = pcpp.part_search("motherboard", limit=num_of_parts, region="de")
    motherboards = []

    for part in parts:
        if part.price is None:
            continue

        url = part.url
        success = False
        attempts = 0
        max_attempts = 3

        while not success and attempts < max_attempts:
            try:
                product = pcpp.fetch_product(url)
                if product is not None and hasattr(product, "specs"):
                    mb_specs = MotherboardSpecs(
                        manufacturer=product.specs.get("Manufacturer", [None]),
                        model=product.specs.get("Model", [None]),
                        part_number=product.specs.get("Part #", [None]),
                        socket_cpu=product.specs.get("Socket / CPU", [None]),
                        chipset=product.specs.get("Chipset", [None]),
                        form_factor=product.specs.get("Form Factor", [None]),
                        memory_type=product.specs.get("Memory Type", [None]),
                        memory_speed=product.specs.get("Memory Speed", [None]),
                        memory_max=product.specs.get("Memory Max", [None]),
                        memory_slots=product.specs.get("Memory Slots", [None]),
                        pcie_slots=product.specs.get("PCIe Slots", [None]),
                        m2_slots=product.specs.get("M.2 Slots", [None]),
                        sata_ports=product.specs.get("SATA 6.0 Gb/s", [None]),
                        usb_ports=product.specs.get("USB Ports", [None]),
                        wireless=product.specs.get("Wireless Networking", [None]),
                        ethernet=product.specs.get("Onboard Ethernet", [None]),
                    )

                    motherboard = Motherboard(url, part.name, part.price, mb_specs)
                    motherboards.append(motherboard.to_dict())
                    success = True
                else:
                    print("Warning: Product data not available.")
                    success = True  # Avoid infinite loop; skip to next part.
            except Exception as e:
                attempts += 1
                print(
                    f"Error fetching product data for {url} (Attempt {attempts}/{max_attempts}): {e}"
                )
                if attempts < max_attempts:
                    time.sleep(5)  # Wait before retrying

        if not success:
            print(f"Failed to fetch product data for {url}.")

    with open("data/mb.json", "w") as f:  # Writing to JSON file
        json.dump(motherboards, f, indent=4)


def loadMBsfromJSON():
    with open("data/mb.json", "r") as f:  # Reading from JSON file
        mb_data = json.load(f)

    return [
        Motherboard(
            data["url"], data["name"], data["price"], MotherboardSpecs(**data["specs"])
        )
        for data in mb_data
    ]
