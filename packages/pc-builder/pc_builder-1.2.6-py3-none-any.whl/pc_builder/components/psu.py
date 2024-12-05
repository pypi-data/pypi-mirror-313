import time
import json
from pypartpicker import Scraper
from pc_builder.compatibility.psu import *


class PSUCompatibility:
    def __init__(self):
        self.compatibilities = {
            "cpu": {
                "tdp": True,
            },
            "gpu": {"tdp": True},
        }
        self.messages = {
            "cpu": [],
            "gpu": [],
        }


class PSUSpecs:
    def __init__(
        self,
        manufacturer,
        model,
        part_numbers,
        psu_type,
        efficiency_rating,
        wattage,
        length,
        modular,
        color,
        fanless,
        atx_4_pin_connectors,
        eps_8_pin_connectors,
        pcie_12_4_pin_connectors,
        pcie_12_pin_connectors,
        pcie_8_pin_connectors,
        pcie_6_2_pin_connectors,
        pcie_6_pin_connectors,
        sata_connectors,
        molex_4_pin_connectors,
    ):
        self.manufacturer = manufacturer
        self.model = model
        self.part_numbers = part_numbers
        self.psu_type = psu_type
        self.efficiency_rating = efficiency_rating
        self.wattage = wattage
        self.length = length
        self.modular = modular
        self.color = color
        self.fanless = fanless
        self.atx_4_pin_connectors = atx_4_pin_connectors
        self.eps_8_pin_connectors = eps_8_pin_connectors
        self.pcie_12_4_pin_connectors = pcie_12_4_pin_connectors
        self.pcie_12_pin_connectors = pcie_12_pin_connectors
        self.pcie_8_pin_connectors = pcie_8_pin_connectors
        self.pcie_6_2_pin_connectors = pcie_6_2_pin_connectors
        self.pcie_6_pin_connectors = pcie_6_pin_connectors
        self.sata_connectors = sata_connectors
        self.molex_4_pin_connectors = molex_4_pin_connectors

    def to_dict(self):
        return self.__dict__


class PSU:
    def __init__(self, url, name, price, psu_specs):
        self.url = url
        self.name = name
        self.price = price
        self.specs = psu_specs  # Pass the PSUSpecs object directly

    def to_dict(self):
        return {
            "url": self.url,
            "name": self.name,
            "price": self.price,
            "specs": self.specs.to_dict(),
        }

    def checkCompatibility(self, userBuild):
        psuComp = PSUCompatibility()
        isCompatible = True

        if not checkPSU_CPU_GPUCompatibility(self, userBuild, psuComp):
            isCompatible = False

        return isCompatible, psuComp


def savePSUsToJSON(pcpp: Scraper, num_of_parts: int):
    parts = pcpp.part_search("power supply", limit=num_of_parts, region="de")
    psus = []

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
                    psu_specs = PSUSpecs(
                        manufacturer=product.specs.get("Manufacturer", [None]),
                        model=product.specs.get("Model", [None]),
                        part_numbers=product.specs.get("Part #", [None]),
                        psu_type=product.specs.get("Type", [None]),
                        efficiency_rating=product.specs.get(
                            "Efficiency Rating", [None]
                        ),
                        wattage=product.specs.get("Wattage", [None]),
                        length=product.specs.get("Length", [None]),
                        modular=product.specs.get("Modular", [None]),
                        color=product.specs.get("Color", [None]),
                        fanless=product.specs.get("Fanless", [None]),
                        atx_4_pin_connectors=product.specs.get(
                            "ATX 4-Pin Connectors", [None]
                        ),
                        eps_8_pin_connectors=product.specs.get(
                            "EPS 8-Pin Connectors", [None]
                        ),
                        pcie_12_4_pin_connectors=product.specs.get(
                            "PCIe 12+4-Pin 12VHPWR Connectors", [None]
                        ),
                        pcie_12_pin_connectors=product.specs.get(
                            "PCIe 12-Pin Connectors", [None]
                        ),
                        pcie_8_pin_connectors=product.specs.get(
                            "PCIe 8-Pin Connectors", [None]
                        ),
                        pcie_6_2_pin_connectors=product.specs.get(
                            "PCIe 6+2-Pin Connectors", [None]
                        ),
                        pcie_6_pin_connectors=product.specs.get(
                            "PCIe 6-Pin Connectors", [None]
                        ),
                        sata_connectors=product.specs.get("SATA Connectors", [None]),
                        molex_4_pin_connectors=product.specs.get(
                            "Molex 4-Pin Connectors", [None]
                        ),
                    )

                    psu = PSU(url, part.name, part.price, psu_specs)
                    psus.append(psu.to_dict())
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

    with open("data/psu.json", "w") as f:  # Writing to JSON file
        json.dump(psus, f, indent=4)


def loadPSUsfromJSON():
    with open("data/psu.json", "r") as f:  # Reading from JSON file
        psu_data = json.load(f)

    return [
        PSU(data["url"], data["name"], data["price"], PSUSpecs(**data["specs"]))
        for data in psu_data
    ]
