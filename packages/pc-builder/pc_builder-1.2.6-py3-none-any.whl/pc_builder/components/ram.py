import time
import json
from pypartpicker import Scraper
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


class RAMSpecs:
    def __init__(
        self,
        manufacturer,
        model,
        part_number,
        speed,
        form_factor,
        modules,
        color,
        first_word_latency,
        cas_latency,
        voltage,
        timing,
        ecc_registered,
        heat_spreader,
    ):
        self.manufacturer = manufacturer
        self.model = model
        self.part_number = part_number
        self.speed = speed
        self.form_factor = form_factor
        self.modules = modules
        self.color = color
        self.first_word_latency = first_word_latency
        self.cas_latency = cas_latency
        self.voltage = voltage
        self.timing = timing
        self.ecc_registered = ecc_registered
        self.heat_spreader = heat_spreader

    def to_dict(self):
        return self.__dict__


class RAM:
    def __init__(self, url, name, price, ram_specs):
        self.url = url
        self.name = name
        self.price = price
        self.specs = ram_specs  # Pass the RAMSpecs object directly

    def to_dict(self):
        return {
            "url": self.url,
            "name": self.name,
            "price": self.price,
            "specs": self.specs.to_dict(),
        }

    def checkCompatibility(self, userBuild):
        ramComp = RAMCompatibility()
        isCompatible = True

        if not checkMultipleRAMDDRCompatibility(self, userBuild, ramComp):
            isCompatible = False

        if not checkRAM_MotherboardCompatibility(self, userBuild, ramComp):
            isCompatible = False

        return isCompatible, ramComp


def saveRAMsToJSON(pcpp: Scraper, num_of_parts: int):
    parts = pcpp.part_search("memory", limit=num_of_parts, region="de")
    rams = []

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
                    ram_specs = RAMSpecs(
                        manufacturer=product.specs.get("Manufacturer", [None]),
                        model=product.specs.get("Model", [None]),
                        part_number=product.specs.get("Part #", [None]),
                        speed=product.specs.get("Speed", [None]),
                        form_factor=product.specs.get("Form Factor", [None]),
                        modules=product.specs.get("Modules", [None]),
                        color=product.specs.get("Color", [None]),
                        first_word_latency=product.specs.get(
                            "First Word Latency", [None]
                        ),
                        cas_latency=product.specs.get("CAS Latency", [None]),
                        voltage=product.specs.get("Voltage", [None]),
                        timing=product.specs.get("Timing", [None]),
                        ecc_registered=product.specs.get("ECC / Registered", [None]),
                        heat_spreader=product.specs.get("Heat Spreader", [None]),
                    )

                    ram = RAM(url, part.name, part.price, ram_specs)
                    rams.append(ram.to_dict())
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

    with open("data/ram.json", "w") as f:  # Writing to JSON file
        json.dump(rams, f, indent=4)


def loadRAMsfromJSON():
    with open("data/ram.json", "r") as f:  # Reading from JSON file
        ram_data = json.load(f)

    return [
        RAM(data["url"], data["name"], data["price"], RAMSpecs(**data["specs"]))
        for data in ram_data
    ]
