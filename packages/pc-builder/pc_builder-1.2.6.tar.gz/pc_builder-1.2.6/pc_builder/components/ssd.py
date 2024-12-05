import time
import json
from pypartpicker import Scraper
from pc_builder.compatibility.ssd import *


class SSDCompatibility:
    def __init__(self):
        self.compatibilities = {
            "motherboard": {
                "interface": True,
                "sata_slots": True,
                "m2_slots": True,
            },
            "case": {
                "drive_bay": True,
            },
        }
        self.messages = {
            "motherboard": [],
            "case": [],
        }


class SSDSpecs:
    def __init__(
        self,
        manufacturer,
        model,
        part_number,
        capacity,
        type,
        cache,
        interface,
        nvme,
        form_factor,
        color,
        rpm,
    ):
        self.manufacturer = manufacturer
        self.model = model
        self.part_number = part_number
        self.capacity = capacity
        self.type = type
        self.cache = cache
        self.interface = interface
        self.nvme = nvme
        self.form_factor = form_factor
        self.color = color
        self.rpm = rpm

    def to_dict(self):
        return self.__dict__


class SSD:
    def __init__(self, url, name, price, ssd_specs):
        self.url = url
        self.name = name
        self.price = price
        self.specs = ssd_specs  # Pass the SSDSpecs object directly

    def to_dict(self):
        return {
            "url": self.url,
            "name": self.name,
            "price": self.price,
            "specs": self.specs.to_dict(),
        }

    def checkCompatibility(self, userBuild):
        ssdComp = SSDCompatibility()
        isCompatible = True

        if not checkSSD_MB_CaseCompatibility(self, userBuild, ssdComp):
            isCompatible = False

        return isCompatible, ssdComp


def saveSSDsToJSON(pcpp: Scraper, num_of_parts: int):
    parts = pcpp.part_search("solid state drive", limit=num_of_parts, region="de")
    ssds = []

    for part in parts:
        if part.price is None:
            continue

        if "external" in part.url.lower() or "external" in part.name.lower():
            print(f"Skipping external SSD: {part.name}")
            continue

        url = part.url
        success = False
        attempts = 0
        max_attempts = 3

        while not success and attempts < max_attempts:
            try:
                product = pcpp.fetch_product(url)
                if product is not None and hasattr(product, "specs"):
                    ssd_specs = SSDSpecs(
                        manufacturer=product.specs.get("Manufacturer", [None]),
                        model=product.specs.get("Model", [None]),
                        part_number=product.specs.get("Part #", [None]),
                        capacity=product.specs.get("Capacity", [None]),
                        type=product.specs.get("Type", [None]),
                        cache=product.specs.get("Cache", [None]),
                        interface=product.specs.get("Interface", [None]),
                        nvme=product.specs.get("NVME", [None]),
                        form_factor=product.specs.get("Form Factor", [None]),
                        color=product.specs.get("Color", [None]),
                        rpm=product.specs.get("RPM", [None]),
                    )

                    ssd = SSD(url, part.name, part.price, ssd_specs)
                    ssds.append(ssd.to_dict())
                    success = True
                else:
                    print(f"Warning: Product data not available for {url}.")
                    success = True  # Move to next part
            except Exception as e:
                attempts += 1
                print(
                    f"Error fetching product data for {url} (Attempt {attempts}/{max_attempts}): {e}"
                )
                if attempts < max_attempts:
                    time.sleep(5)  # Wait before retrying

        if not success:
            print(f"Failed to fetch product data for {url}.")

    with open("data/ssd.json", "w") as f:  # Writing to JSON file
        json.dump(ssds, f, indent=4)


def loadSSDsfromJSON():
    with open("data/ssd.json", "r") as f:  # Reading from JSON file
        ssd_data = json.load(f)

    return [
        SSD(data["url"], data["name"], data["price"], SSDSpecs(**data["specs"]))
        for data in ssd_data
    ]
