import time
import json
from pypartpicker import Scraper
from pc_builder.compatibility.cpucooler import *


class CPUCoolerCompatibility:
    def __init__(self):
        self.compatibilities = {
            "cpu": {
                "socket": True,
            },
        }
        self.messages = {
            "cpu": [],
        }


class CPUCoolerSpecs:
    def __init__(
        self,
        manufacturer,
        model,
        part_numbers,
        fan_rpm,
        noise_level,
        color,
        height,
        cpu_sockets,
        water_cooled,
        fanless,
    ):
        self.manufacturer = manufacturer
        self.model = model
        self.part_numbers = part_numbers
        self.fan_rpm = fan_rpm
        self.noise_level = noise_level
        self.color = color
        self.height = height
        self.cpu_sockets = cpu_sockets
        self.water_cooled = water_cooled
        self.fanless = fanless

    def to_dict(self):
        return self.__dict__


class CPUCooler:
    def __init__(self, url, name, price, cpu_cooler_specs):
        self.url = url
        self.name = name
        self.price = price
        self.specs = cpu_cooler_specs  # Pass the CPUCoolerSpecs object directly

    def to_dict(self):
        return {
            "url": self.url,
            "name": self.name,
            "price": self.price,
            "specs": self.specs.to_dict(),
        }

    def checkCompatibility(self, userBuild):
        cpuCoolerComp = CPUCoolerCompatibility()
        isCompatible = True

        if not checkCPUCooler_CPUCompatibility(self, userBuild, cpuCoolerComp):
            isCompatible = False

        return isCompatible, cpuCoolerComp


def saveCPUCoolersToJSON(pcpp: Scraper, num_of_parts: int):
    parts = pcpp.part_search("cpu cooler", limit=num_of_parts, region="de")
    cpu_coolers = []

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
                    # Create CPUCoolerSpecs with individual values from product.specs
                    cpu_cooler_specs = CPUCoolerSpecs(
                        manufacturer=product.specs.get("Manufacturer", [None]),
                        model=product.specs.get("Model", [None]),
                        part_numbers=product.specs.get("Part #", [None]),
                        fan_rpm=product.specs.get("Fan RPM", [None]),
                        noise_level=product.specs.get("Noise Level", [None]),
                        color=product.specs.get("Color", [None]),
                        height=product.specs.get("Height", [None]),
                        cpu_sockets=product.specs.get("CPU Socket", [None]),
                        water_cooled=product.specs.get("Water Cooled", [None]),
                        fanless=product.specs.get("Fanless", [None]),
                    )

                    cpu_cooler = CPUCooler(url, part.name, part.price, cpu_cooler_specs)
                    cpu_coolers.append(cpu_cooler.to_dict())
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

    with open("data/cpuCooler.json", "w") as f:  # Writing to JSON file
        json.dump(cpu_coolers, f, indent=4)


def loadCPUCoolersfromJSON():
    with open("data/cpuCooler.json", "r") as f:  # Reading from JSON file
        cpu_cooler_data = json.load(f)

    return [
        CPUCooler(
            data["url"], data["name"], data["price"], CPUCoolerSpecs(**data["specs"])
        )
        for data in cpu_cooler_data
    ]
