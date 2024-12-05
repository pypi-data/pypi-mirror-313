import time
import json
from pypartpicker import Scraper
from pc_builder.compatibility.case import *


class CaseCompatibility:
    def __init__(self):
        self.compatibilities = {
            "motherboard": {
                "form_factor": True,
            },
            "gpu": {
                "length": True,
            },
            "hdd": {
                "drive_bay": True,
            },
            "ssd": {
                "drive_bay": True,
            },
        }
        self.messages = {
            "motherboard": [],
            "gpu": [],
            "hdd": [],
            "ssd": [],
        }


class CaseSpecs:
    def __init__(
        self,
        manufacturer,
        part_number,
        case_type,
        color,
        power_supply,
        side_panel,
        power_supply_shroud,
        front_panel_usb,
        motherboard_form_factor,
        max_gpu_length,
        drive_bays,
        expansion_slots,
        dimensions,
        volume,
    ):
        self.manufacturer = manufacturer
        self.part_number = part_number
        self.case_type = case_type
        self.color = color
        self.power_supply = power_supply
        self.side_panel = side_panel
        self.power_supply_shroud = power_supply_shroud
        self.front_panel_usb = front_panel_usb
        self.motherboard_form_factor = motherboard_form_factor
        self.max_gpu_length = max_gpu_length
        self.drive_bays = drive_bays
        self.expansion_slots = expansion_slots
        self.dimensions = dimensions
        self.volume = volume

    def to_dict(self):
        return self.__dict__


class Case:
    def __init__(self, url, name, price, case_specs):
        self.url = url
        self.name = name
        self.price = price
        self.specs = case_specs

    def to_dict(self):
        return {
            "url": self.url,
            "name": self.name,
            "price": self.price,
            "specs": self.specs.to_dict(),
        }

    def checkCompatibility(self, userBuild):
        caseComp = CaseCompatibility()
        isCompatible = True

        if not checkCase_MBCompatibility(self, userBuild, caseComp):
            isCompatible = False

        if not checkCase_GPUCompatibility(self, userBuild, caseComp):
            isCompatible = False

        if not checkCase_HDDCompatibility(self, userBuild, caseComp):
            isCompatible = False

        if not checkCase_SSDCompatibility(self, userBuild, caseComp):
            isCompatible = False

        return isCompatible, caseComp


def saveCasesToJSON(pcpp: Scraper, numOfParts: int):
    parts = pcpp.part_search("case", limit=numOfParts, region="de")
    cases = []

    for part in parts:
        if part.price is None:
            continue

        if "controller" in part.url.lower() or "controller" in part.name.lower():
            print(f"Skipping controller in cases: {part.name}")
            continue

        url = part.url
        success = False
        attempts = 0
        max_attempts = 3

        while not success and attempts < max_attempts:
            try:
                product = pcpp.fetch_product(url)
                if product is not None and hasattr(product, "specs"):
                    case_specs = CaseSpecs(
                        manufacturer=product.specs.get("Manufacturer", [None]),
                        part_number=product.specs.get("Part #", [None]),
                        case_type=product.specs.get("Type", [None]),
                        color=product.specs.get("Color", [None]),
                        power_supply=product.specs.get("Power Supply", [None]),
                        side_panel=product.specs.get("Side Panel", [None]),
                        power_supply_shroud=product.specs.get(
                            "Power Supply Shroud", [None]
                        ),
                        front_panel_usb=product.specs.get("Front Panel USB", [None]),
                        motherboard_form_factor=product.specs.get(
                            "Motherboard Form Factor", [None]
                        ),
                        max_gpu_length=product.specs.get(
                            "Maximum Video Card Length", [None]
                        ),
                        drive_bays=product.specs.get("Drive Bays", [None]),
                        expansion_slots=product.specs.get("Expansion Slots", [None]),
                        dimensions=product.specs.get("Dimensions", [None]),
                        volume=product.specs.get("Volume", [None]),
                    )

                    case = Case(url, part.name, part.price, case_specs)
                    cases.append(case.to_dict())
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

    with open("data/case.json", "w") as f:  # Writing to JSON file
        json.dump(cases, f, indent=4)


def loadCasesfromJSON():
    with open("data/case.json", "r") as f:  # Reading from JSON file
        case_data = json.load(f)

    return [
        Case(data["url"], data["name"], data["price"], CaseSpecs(**data["specs"]))
        for data in case_data
    ]
