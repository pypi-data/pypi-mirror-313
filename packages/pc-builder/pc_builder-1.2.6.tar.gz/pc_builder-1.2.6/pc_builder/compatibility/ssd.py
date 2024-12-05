def checkSSD_MB_CaseCompatibility(ssd, userBuild, ssdComp):
    if "motherboard" not in ssdComp.messages:
        ssdComp.messages["motherboard"] = []
    if "case" not in ssdComp.messages:
        ssdComp.messages["case"] = []

    if not ssd:
        ssdComp.messages["motherboard"].append(
            "No SSD specified for compatibility check."
        )
        return False

    ssdFormFactor = ssd.specs.form_factor[0].split("-")[-1]
    interfaceType = ssd.specs.interface[0]

    if "M.2" in interfaceType:
        motherboard = userBuild.components.get("motherboard")
        if motherboard:
            mb = motherboard[0]
            mbM2Slots = [slot for slot in mb.specs.m2_slots if "E-key" not in slot]
            totalM2Slots = len(mbM2Slots)
            m2DeviceAmount = 0
            ssds = userBuild.components.get("ssd")
            for ssd in ssds:
                if "M.2" in ssd.specs.interface[0]:
                    m2DeviceAmount += 1

            if m2DeviceAmount >= totalM2Slots:
                ssdComp.compatibilities["motherboard"]["m2_slots"] = False
                ssdComp.messages["motherboard"].append(
                    f"Incompatible motherboard: '{mb.name}' has {totalM2Slots} M2 slots, "
                    f"but you are trying to add {m2DeviceAmount + 1} SSD(s) that use M2 slots"
                )
                return False

            if any(ssdFormFactor in slot for slot in mbM2Slots):
                return True
            else:
                ssdComp.compatibilities["motherboard"]["interface"] = False
                ssdComp.messages["motherboard"].append(
                    f"Incompatible SSD: The M.2 SSD form factor ({ssdFormFactor}) is not supported "
                    f"by any M.2 slots on the motherboard '{mb.name}'."
                )
                return False

    elif "SATA" in interfaceType:
        motherboard = userBuild.components.get("motherboard")
        if motherboard:

            mb = motherboard[0]
            numOfSataPorts = int(mb.specs.sata_ports[0])
            sataDeviceAmount = len(userBuild.components.get("hdd", []))

            ssds = userBuild.components.get("ssd")
            for ssd in ssds:
                if "SATA" in ssd.specs.interface[0]:
                    sataDeviceAmount += 1

            if sataDeviceAmount >= numOfSataPorts:
                ssdComp.compatibilities["motherboard"]["sata_slots"] = False
                ssdComp.messages["motherboard"].append(
                    f"Incompatible motherboard: '{mb.name}' has {numOfSataPorts} SATA ports, "
                    f"but you are trying to add {sataDeviceAmount + 1}th SSD that connects through {interfaceType}."
                )
                return False
        case = userBuild.components.get("case")
        if case:

            if any(ssdFormFactor in bay for bay in case[0].specs.drive_bays):
                return True
            else:
                ssdComp.compatibilities["case"]["drive_bay"] = False
                ssdComp.messages["case"].append(
                    f"Incompatible SSD: The SSD form factor ({ssdFormFactor}) is not compatible "
                    f"with any drive bays in the case '{case[0].name}'."
                )
                return False

    return True
