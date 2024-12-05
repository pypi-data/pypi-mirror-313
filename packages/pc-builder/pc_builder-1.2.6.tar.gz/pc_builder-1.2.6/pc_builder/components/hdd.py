import time
import json
from pypartpicker import Scraper
from pc_builder.compatibility.hdd import *


class HDDCompatibility:
    def __init__(self):
        self.compatibilities = {
            "motherboard": {
                "slots": True,
            },
            "case": {
                "drive_bay": True,
            },
        }
        self.messages = {
            "motherboard": [],
            "case": [],
        }


class HDDSpecs:
    def __init__(
        self,
        manufacturer,
        model,
        part_number,
        capacity,
        drive_type,
        cache,
        interface,
        form_factor,
        nvme,
        color,
        rpm,
    ):
        self.manufacturer = manufacturer
        self.model = model
        self.part_number = part_number
        self.capacity = capacity
        self.drive_type = drive_type
        self.cache = cache
        self.interface = interface
        self.form_factor = form_factor
        self.nvme = nvme
        self.color = color
        self.rpm = rpm

    def to_dict(self):
        return self.__dict__


class HDD:
    def __init__(self, url, name, price, hdd_specs):
        self.url = url
        self.name = name
        self.price = price
        self.specs = hdd_specs  # Pass the HDDSpecs object directly

    def to_dict(self):
        return {
            "url": self.url,
            "name": self.name,
            "price": self.price,
            "specs": self.specs.to_dict(),
        }

    def checkCompatibility(self, userBuild):
        hddComp = HDDCompatibility()
        isCompatible = True

        if not checkHDD_MB_CaseCompatibility(self, userBuild, hddComp):
            isCompatible = False

        return isCompatible, hddComp


def saveHDDsToJSON(pcpp: Scraper, num_of_parts: int):
    parts = pcpp.part_search("internal hard drive", limit=num_of_parts, region="de")
    hdds = []

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
                    # Create HDDSpecs with individual values from product.specs
                    hdd_specs = HDDSpecs(
                        manufacturer=product.specs.get("Manufacturer", [None]),
                        model=product.specs.get("Model", [None]),
                        part_number=product.specs.get("Part #", [None]),
                        capacity=product.specs.get("Capacity", [None]),
                        drive_type=product.specs.get("Type", [None]),
                        cache=product.specs.get("Cache", [None]),
                        interface=product.specs.get("Interface", [None]),
                        form_factor=product.specs.get("Form Factor", [None]),
                        nvme=product.specs.get("NVME", [None]),
                        color=product.specs.get("Color", [None]),
                        rpm=product.specs.get("RPM", [None]),
                    )

                    hdd = HDD(url, part.name, part.price, hdd_specs)
                    hdds.append(hdd.to_dict())
                    success = True
                else:
                    print(f"Warning: Product data not available for {url}.")
                    success = True  # Avoid infinite loop; skip to next part
            except Exception as e:
                attempts += 1
                print(
                    f"Error fetching product data for {url} (Attempt {attempts}/{max_attempts}): {e}"
                )
                if attempts < max_attempts:
                    time.sleep(5)  # Wait before retrying

        if not success:
            print(f"Failed to fetch product data for {url}.")

    with open("data/hdd.json", "w") as f:  # Writing to JSON file
        json.dump(hdds, f, indent=4)


def loadHDDsfromJSON():
    with open("data/hdd.json", "r") as f:  # Reading from JSON file
        hdd_data = json.load(f)

    return [
        HDD(data["url"], data["name"], data["price"], HDDSpecs(**data["specs"]))
        for data in hdd_data
    ]
