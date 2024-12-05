import time
import json
from pypartpicker import Scraper
from pc_builder.compatibility.cpu import *


class CPUCompatibility:
    def __init__(self):
        self.compatibilities = {
            "motherboard": {
                "socket_cpu": True,
            },
            "cpucooler": {
                "cpu_sockets": True,
            },
            "psu": {"wattage": True},
        }
        self.messages = {
            "motherboard": [],
            "cpucooler": [],
            "psu": [],
        }


class CPUSpecs:
    def __init__(
        self,
        manufacturer,
        model,
        part_number,
        socket_type,
        core_count,
        thread_count,
        base_clock,
        boost_clock,
        tdp,
        integrated_graphics,
        smt_support,
    ):
        self.manufacturer = manufacturer
        self.model = model
        self.part_number = part_number
        self.socket_type = socket_type
        self.core_count = core_count
        self.thread_count = thread_count
        self.base_clock = base_clock
        self.boost_clock = boost_clock
        self.tdp = tdp
        self.integrated_graphics = integrated_graphics
        self.smt_support = smt_support

    def to_dict(self):
        return self.__dict__


class CPU:
    def __init__(self, url, name, price, cpu_specs):
        self.url = url
        self.name = name
        self.price = price
        self.specs = cpu_specs  # Pass the CPUSpecs object directly

    def to_dict(self):
        return {
            "url": self.url,
            "name": self.name,
            "price": self.price,
            "specs": self.specs.to_dict(),
        }

    def checkCompatibility(self, userBuild):
        cpuComp = CPUCompatibility()
        isCompatible = True

        if not checkCPU_MotherboardCompatibility(self, userBuild, cpuComp):
            isCompatible = False

        if not checkCPU_CPUCoolerCompatibility(self, userBuild, cpuComp):
            isCompatible = False

        if not checkCPU_PSUCompatibility(self, userBuild, cpuComp):
            isCompatible = False

        return isCompatible, cpuComp


def saveCPUsToJSON(pcpp: Scraper, num_of_parts: int):
    parts = pcpp.part_search("processor", limit=num_of_parts, region="de")
    cpus = []

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
                    cpu_specs = CPUSpecs(
                        manufacturer=product.specs.get("Manufacturer", [None]),
                        model=product.specs.get("Model", [None]),
                        part_number=product.specs.get("Part #", [None]),
                        socket_type=product.specs.get("Socket", [None]),
                        core_count=product.specs.get("Core Count", [None]),
                        thread_count=product.specs.get("Thread Count", [None]),
                        base_clock=product.specs.get("Base Clock", [None]),
                        boost_clock=product.specs.get("Boost Clock", [None]),
                        tdp=product.specs.get("TDP", [None]),
                        integrated_graphics=product.specs.get(
                            "Integrated Graphics", [None]
                        ),
                        smt_support=product.specs.get("SMT", [None]),
                    )

                    cpu = CPU(url, part.name, part.price, cpu_specs)
                    cpus.append(cpu.to_dict())
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

    with open("data/cpu.json", "w") as f:  # Writing to JSON file
        json.dump(cpus, f, indent=4)


def loadCPUsfromJSON():
    with open("data/cpu.json", "r") as f:  # Reading from JSON file
        cpu_data = json.load(f)

    return [
        CPU(data["url"], data["name"], data["price"], CPUSpecs(**data["specs"]))
        for data in cpu_data
    ]
