def checkRAM_MotherboardCompatibility(ram, userBuild, ramComp):
    if "motherboard" not in ramComp.messages:
        ramComp.messages["motherboard"] = []

    if not userBuild.components.get("motherboard"):
        ramComp.messages["motherboard"].append(
            "No motherboard specified for compatibility check."
        )
        return True

    motherboard = userBuild.components["motherboard"][0]
    motherboardMem = motherboard.specs.memory_speed
    motherboardLimit = int(motherboard.specs.memory_max[0].split()[0])
    motherboardSlots = int(motherboard.specs.memory_slots[0])

    ramMem = ram.specs.speed[0]
    ramStr = ram.specs.modules[0]
    ramAmount = int(ramStr.split(" x ")[0])
    ramCapacity = int(ramStr.split(" x ")[1][:-2])

    totalCapacity = ramCapacity * ramAmount

    if userBuild.components.get("ram"):
        existingRamCount = 0
        existingTotalCapacity = 0

        for stick in userBuild.components["ram"]:
            stickStr = stick.specs.modules[0]
            stickAmount = int(stickStr.split(" x ")[0])
            stickCapacity = int(stickStr.split(" x ")[1][:-2])

            existingTotalCapacity += stickAmount * stickCapacity
            existingRamCount += stickAmount

        totalCapacity += existingTotalCapacity
        ramAmount += existingRamCount

    if ramAmount > motherboardSlots:
        ramComp.compatibilities["motherboard"]["memory_slots"] = False
        ramComp.messages["motherboard"].append(
            f"Incompatible RAM: The total number of RAM sticks ({ramAmount}) exceeds the "
            f"motherboard's available slots ({motherboardSlots})."
        )
        return False

    if totalCapacity > motherboardLimit:
        ramComp.compatibilities["motherboard"]["memory_max"] = False
        ramComp.messages["motherboard"].append(
            f"Incompatible RAM: The total RAM capacity ({totalCapacity} GB) exceeds the "
            f"motherboard's maximum capacity ({motherboardLimit} GB)."
        )
        return False

    if ramMem not in motherboardMem:
        ramComp.compatibilities["motherboard"]["memory_speed"] = False
        ramComp.messages["motherboard"].append(
            f"Incompatible RAM: The RAM speed ({ramMem}) is not supported by the motherboard's "
            f"memory speeds ({', '.join(motherboardMem)})."
        )
        return False

    return True


def checkMultipleRAMDDRCompatibility(ram, userBuild, ramComp):
    if len(userBuild.components["ram"]) == 0:
        return True
    firstRAM = userBuild.components["ram"][0]

    firstRAMSpeedStr = firstRAM.specs.speed[0]
    firstRAMDDR = firstRAMSpeedStr.split("-")[0]

    newRAMSpeedStr = ram.specs.speed[0]
    newRAMDDR = newRAMSpeedStr.split("-")[0]

    if firstRAMDDR != newRAMDDR:
        ramComp.compatibilities["ram"]["ddr"] = False
        ramComp.messages["ram"].append(
            f"Incompatible RAM: The RAM DDR ({newRAMDDR}) is different from existing RAM'S DDR ({firstRAMDDR})"
        )
        return False

    return True
