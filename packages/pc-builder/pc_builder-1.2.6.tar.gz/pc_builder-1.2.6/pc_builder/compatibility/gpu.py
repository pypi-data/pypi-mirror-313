def checkGPU_PSUCompatibility(gpu, userBuild, gpuComp):
    gpuComp.messages["psu"] = []
    psu = userBuild.components.get("psu")
    if not psu:
        return True

    psu = psu[0]
    psuWattage = float(psu.specs.wattage[0].split(" ")[0])
    gpuTDP = float(gpu.specs.tdp[0].split(" ")[0])
    cpuTDP = 0

    if userBuild.components.get("cpu"):
        cpu = userBuild.components["cpu"][0]
        cpuTDP = float(cpu.specs.tdp[0].split(" ")[0])

    totalPowerConsumption = gpuTDP + cpuTDP

    if totalPowerConsumption <= psuWattage:
        return True

    gpuComp.compatibilities["psu"]["wattage"] = False
    gpuComp.messages["psu"].append(
        f"Incompatible PSU: '{psu.name}' has insufficient wattage. "
        f"Required: {totalPowerConsumption}W, Available: {psuWattage}W."
    )
    return False


def checkGPU_CaseCompatibility(gpu, userBuild, gpuComp):
    gpuComp.messages["case"] = []
    case = userBuild.components.get("case")
    if not case:
        return True

    case = case[0]
    maxCaseLength = float(case.specs.max_gpu_length[0].split(" ")[0])
    gpuLength = float(gpu.specs.length[0].split(" ")[0])

    if gpuLength <= maxCaseLength:
        return True

    gpuComp.compatibilities["case"]["length"] = False
    gpuComp.messages["case"].append(
        f"Incompatible case: '{case.name}' is too short for GPU '{gpu.name}'. "
        f"GPU Length: {gpuLength}mm, Maximum Case Length: {maxCaseLength}mm."
    )
    return False
