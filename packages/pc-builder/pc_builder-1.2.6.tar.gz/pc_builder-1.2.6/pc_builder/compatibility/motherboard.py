def checkMotherboard_RAMCompatibility(motherboard, userBuild, motherboardComp):
    if not userBuild.components["ram"]:
        return True

    motherboardMem = motherboard.specs.memory_speed
    motherboardStr = motherboard.specs.memory_max[0]
    motherboardLimit = int(motherboardStr.split()[0])
    motherboardSlots = int(motherboard.specs.memory_slots[0])

    totalCapacity = 0
    ramAmount = 0
    incompatibleRams = []

    if "ram" not in motherboardComp.messages:
        motherboardComp.messages["ram"] = []

    for stick in userBuild.components["ram"]:
        stickName = stick.name
        stickStr = stick.specs.modules[0]
        stickAmount, stickCapacityStr = stickStr.split(" x ")
        stickAmount = int(stickAmount)
        stickCapacity = int(stickCapacityStr[:-2])
        stickSpeed = stick.specs.speed[0]

        totalCapacity += stickAmount * stickCapacity
        ramAmount += stickAmount

        if stickSpeed not in motherboardMem:
            incompatibleRams.append(stickName)
            motherboardComp.messages["ram"].append(
                f"Incompatible RAM: '{stickName}' has a speed of '{stickSpeed}', "
                f"but the motherboard supports speeds: {motherboardMem}."
            )

    if motherboardSlots < ramAmount:
        motherboardComp.compatibilities["ram"]["slots"] = False
        motherboardComp.messages["ram"].append(
            f"Not enough RAM slots: The motherboard has {motherboardSlots} slots, "
            f"but you are trying to use {ramAmount} sticks."
        )
        return False

    if motherboardLimit < totalCapacity:
        motherboardComp.compatibilities["ram"]["capacity"] = False
        motherboardComp.messages["ram"].append(
            f"Memory capacity exceeded: The maximum allowed is {motherboardLimit} GB, "
            f"but the total capacity being used is {totalCapacity} GB."
        )
        return False

    if incompatibleRams:
        motherboardComp.compatibilities["ram"]["speed"] = incompatibleRams
        return False

    return True


def checkMotherboard_CPUCompatibility(motherboard, userBuild, motherboardComp):
    if not userBuild.components["cpu"]:
        return True

    cpu = userBuild.components["cpu"][0]
    cpuSocket = cpu.specs.socket_type[0]
    mbSocket = motherboard.specs.socket_cpu[0]

    if "cpu" not in motherboardComp.messages:
        motherboardComp.messages["cpu"] = []

    if cpuSocket != mbSocket:
        motherboardComp.compatibilities["cpu"]["socket_type"] = False
        motherboardComp.messages["cpu"].append(
            f"Incompatible CPU: '{cpu.name}' socket '{cpuSocket}' does not match "
            f"motherboard socket '{mbSocket}'."
        )
        return False

    return True


def checkMotherboard_CaseCompatibility(motherboard, userBuild, motherboardComp):
    if not userBuild.components["case"]:
        return True

    case = userBuild.components["case"][0]
    caseForms = case.specs.motherboard_form_factor
    mbForm = motherboard.specs.form_factor[0]

    if "case" not in motherboardComp.messages:
        motherboardComp.messages["case"] = []

    if mbForm not in caseForms:
        motherboardComp.compatibilities["case"]["motherboard_form_factor"] = False
        motherboardComp.messages["case"].append(
            f"Incompatible case: '{case.name}' does not support motherboard form factor '{mbForm}'."
        )
        return False

    return True


def checkMotherboard_SSD_HDDCompatibility(motherboard, userBuild, motherboardComp):
    if not userBuild.components["ssd"] and not userBuild.components["hdd"]:
        return True

    motherboardSlots = [
        slot for slot in motherboard.specs.m2_slots if "E-key" not in slot
    ]
    totalM2Slots = len(motherboardSlots)
    totalSataPorts = int(motherboard.specs.sata_ports[0])

    ssdAmount = 0
    sataDeviceAmount = 0
    incompatibleSSDs = []

    if "ssd" not in motherboardComp.messages:
        motherboardComp.messages["ssd"] = []
    if "hdd" not in motherboardComp.messages:
        motherboardComp.messages["hdd"] = []

    for ssd in userBuild.components["ssd"]:
        ssdName = ssd.name
        interfaceType = ssd.specs.interface[0]

        if "M.2" in interfaceType:
            ssdAmount += 1
            ssdForm = ssd.specs.form_factor[0].split("-")[1]

            slotCompatible = any(ssdForm in slot for slot in motherboardSlots)

            if not slotCompatible:
                incompatibleSSDs.append(ssdName)
                motherboardComp.messages["ssd"].append(
                    f"Incompatible SSD: '{ssdName}' form factor '{ssdForm}' is not supported by the motherboard."
                )

        elif "SATA" in interfaceType:
            sataDeviceAmount += 1

    sataDeviceAmount += len(userBuild.components["hdd"])

    if totalM2Slots < ssdAmount:
        motherboardComp.compatibilities["ssd"]["slots"] = False
        motherboardComp.messages["ssd"].append(
            f"Not enough M.2 slots: The motherboard has {totalM2Slots} slots, "
            f"but you are trying to use {ssdAmount} SSD(s)."
        )
        return False

    if totalSataPorts < sataDeviceAmount:
        motherboardComp.compatibilities["hdd"]["ports"] = False
        motherboardComp.messages["hdd"].append(
            f"Not enough SATA ports: The motherboard has {totalSataPorts} SATA ports, "
            f"but you are trying to use {sataDeviceAmount} devices (HDDs and SSDs combined)."
        )
        return False

    if incompatibleSSDs:
        motherboardComp.compatibilities["ssd"]["form_factor"] = incompatibleSSDs
        return False

    return True
