def checkHDD_MB_CaseCompatibility(hdd, userBuild, hddComp):
    if "motherboard" not in hddComp.messages:
        hddComp.messages["motherboard"] = []
    if "case" not in hddComp.messages:
        hddComp.messages["case"] = []

    motherboardSlotCompatible = True
    caseFactorCompatible = True

    if userBuild.components.get("motherboard"):
        mb = userBuild.components["motherboard"][0]
        sataDeviceAmount = len(userBuild.components.get("hdd", []))
        ssds = userBuild.components.get("ssd")
        for ssd in ssds:
            if "SATA" in ssd.specs.interface[0]:
                sataDeviceAmount += 1
        numOfSataPorts = int(mb.specs.sata_ports[0])

        if sataDeviceAmount >= numOfSataPorts:
            hddComp.compatibilities["motherboard"]["slots"] = False
            motherboardSlotCompatible = False
            hddComp.messages["motherboard"].append(
                f"Incompatible motherboard: '{mb.name}' has {numOfSataPorts} SATA ports, "
                f"but you are trying to add {sataDeviceAmount + 1}th HDD(s)."
            )

    if userBuild.components.get("case"):
        hddFormFactor = hdd.specs.form_factor[0]
        case = userBuild.components["case"][0]

        if not any(hddFormFactor in bay for bay in case.specs.drive_bays):
            hddComp.compatibilities["case"]["drive_bay"] = False
            caseFactorCompatible = False
            hddComp.messages["case"].append(
                f"Incompatible case: '{case.name}' does not support HDD form factor '{hddFormFactor}'. "
                f"Supported drive bays: {', '.join(case.specs.drive_bays)}."
            )

    return motherboardSlotCompatible and caseFactorCompatible
