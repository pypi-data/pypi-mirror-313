def checkCase_MBCompatibility(case, userBuild, caseComp):
    mb = userBuild.components.get("motherboard")
    if not mb:
        return True

    mb = mb[0]
    mbFormFactor = mb.specs.form_factor[0]

    if mbFormFactor in case.specs.motherboard_form_factor:
        return True

    message = (
        f"Motherboard '{mb.name}' with form factor '{mbFormFactor}' is incompatible "
        f"with case '{case.name}', which supports form factors: {', '.join(case.specs.motherboard_form_factor)}."
    )
    caseComp.messages["motherboard"].append(message)
    caseComp.compatibilities["motherboard"]["form_factor"] = False
    return False


def checkCase_GPUCompatibility(case, userBuild, caseComp):
    gpu = userBuild.components.get("gpu")
    if not gpu:
        return True

    maxCaseLength = float(case.specs.max_gpu_length[0].split(" ")[0])

    gpu = gpu[0]
    gpuLength = float(gpu.specs.length[0].split(" ")[0])

    if gpuLength <= maxCaseLength:
        return True

    message = (
        f"GPU '{gpu.name}' with length '{gpu.specs.length[0]}' is too long for case '{case.name}', "
        f"which supports a maximum GPU length of '{case.specs.max_gpu_length[0]}'."
    )
    caseComp.messages["gpu"].append(message)
    caseComp.compatibilities["gpu"]["length"] = False
    return False


def checkCase_HDDCompatibility(case, userBuild, caseComp):
    incompatibleHDDs = []

    for hdd in userBuild.components.get("hdd", []):
        hddFormFactor = hdd.specs.form_factor[0]

        if not any(hddFormFactor in bay for bay in case.specs.drive_bays):
            incompatibleHDDs.append(hdd.name)

    if incompatibleHDDs:
        message = (
            f"HDDs {', '.join(incompatibleHDDs)} are incompatible with case '{case.name}' "
            f"drive bays: {', '.join(case.specs.drive_bays)}."
        )
        caseComp.messages["hdd"].append(message)
        caseComp.compatibilities["hdd"]["form_factor"] = incompatibleHDDs
        return False

    return True


def checkCase_SSDCompatibility(case, userBuild, caseComp):
    incompatibleSSDs = []

    for ssd in userBuild.components.get("ssd", []):
        interfaceType = ssd.specs.interface[0]

        if "SATA" in interfaceType:
            ssdFormFactor = ssd.specs.form_factor[0]

            if not any(ssdFormFactor in bay for bay in case.specs.drive_bays):
                incompatibleSSDs.append(ssd.name)

    if incompatibleSSDs:
        message = (
            f"SSDs {', '.join(incompatibleSSDs)} are incompatible with case '{case.name}' "
            f"drive bays: {', '.join(case.specs.drive_bays)}."
        )
        caseComp.messages["ssd"].append(message)
        caseComp.compatibilities["ssd"]["form_factor"] = incompatibleSSDs
        return False

    return True
