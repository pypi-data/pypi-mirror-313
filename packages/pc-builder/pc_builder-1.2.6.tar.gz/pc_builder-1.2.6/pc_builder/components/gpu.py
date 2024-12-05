import time
import json
from pypartpicker import Scraper
from pc_builder.compatibility.gpu import *


class GPUCompatibility:
    def __init__(self):
        self.compatibilities = {
            "psu": {
                "wattage": True,
            },
            "case": {
                "length": True,
            },
        }
        # Change to a dictionary
        self.messages = {"psu": [], "case": []}


class GPUSpecs:
    def __init__(
        self,
        manufacturer,
        model,
        part_number,
        chipset,
        memory,
        memory_type,
        core_clock,
        boost_clock,
        effective_memory_clock,
        interface,
        color,
        frame_sync,
        length,
        tdp,
        case_expansion_slot_width,
        total_slot_width,
        cooling,
        external_power,
        hdmi_outputs,
        displayport_outputs,
    ):
        self.manufacturer = manufacturer
        self.model = model
        self.part_number = part_number
        self.chipset = chipset
        self.memory = memory
        self.memory_type = memory_type
        self.core_clock = core_clock
        self.boost_clock = boost_clock
        self.effective_memory_clock = effective_memory_clock
        self.interface = interface
        self.color = color
        self.frame_sync = frame_sync
        self.length = length
        self.tdp = tdp
        self.case_expansion_slot_width = case_expansion_slot_width
        self.total_slot_width = total_slot_width
        self.cooling = cooling
        self.external_power = external_power
        self.hdmi_outputs = hdmi_outputs
        self.displayport_outputs = displayport_outputs

    def to_dict(self):
        return self.__dict__


class GPU:
    def __init__(self, url, name, price, gpu_specs):
        self.url = url
        self.name = name
        self.price = price
        self.specs = gpu_specs  # Pass the GPUSpecs object directly

    def to_dict(self):
        return {
            "url": self.url,
            "name": self.name,
            "price": self.price,
            "specs": self.specs.to_dict(),
        }

    def checkCompatibility(self, userBuild):
        gpuComp = GPUCompatibility()
        isCompatible = True

        if not checkGPU_CaseCompatibility(self, userBuild, gpuComp):
            isCompatible = False

        if not checkGPU_PSUCompatibility(self, userBuild, gpuComp):
            isCompatible = False

        return isCompatible, gpuComp


def saveGPUsToJson(pcpp: Scraper, num_of_parts: int):
    parts = pcpp.part_search("video card", limit=num_of_parts, region="de")
    gpus = []

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
                    gpu_specs = GPUSpecs(
                        manufacturer=product.specs.get("Manufacturer", [None]),
                        model=product.specs.get("Model", [None]),
                        part_number=product.specs.get("Part #", [None]),
                        chipset=product.specs.get("Chipset", [None]),
                        memory=product.specs.get("Memory", [None]),
                        memory_type=product.specs.get("Memory Type", [None]),
                        core_clock=product.specs.get("Core Clock", [None]),
                        boost_clock=product.specs.get("Boost Clock", [None]),
                        effective_memory_clock=product.specs.get(
                            "Effective Memory Clock", [None]
                        ),
                        interface=product.specs.get("Interface", [None]),
                        color=product.specs.get("Color", [None]),
                        frame_sync=product.specs.get("Frame Sync", [None]),
                        length=product.specs.get("Length", [None]),
                        tdp=product.specs.get("TDP", [None]),
                        case_expansion_slot_width=product.specs.get(
                            "Case Expansion Slot Width", [None]
                        ),
                        total_slot_width=product.specs.get("Total Slot Width", [None]),
                        cooling=product.specs.get("Cooling", [None]),
                        external_power=product.specs.get("External Power", [None]),
                        hdmi_outputs=product.specs.get("HDMI Outputs", [None]),
                        displayport_outputs=product.specs.get(
                            "DisplayPort Outputs", [None]
                        ),
                    )

                    gpu = GPU(url, part.name, part.price, gpu_specs)
                    gpus.append(gpu.to_dict())
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

    with open("data/gpu.json", "w") as f:  # Writing to JSON file
        json.dump(gpus, f, indent=4)


def loadGPUsfromJSON():
    with open("data/gpu.json", "r") as f:  # Reading from JSON file
        gpu_data = json.load(f)

    return [
        GPU(data["url"], data["name"], data["price"], GPUSpecs(**data["specs"]))
        for data in gpu_data
    ]
