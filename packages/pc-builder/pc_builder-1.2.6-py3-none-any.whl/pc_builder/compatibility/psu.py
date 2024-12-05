def checkPSU_CPU_GPUCompatibility(psu, userBuild, psuComp):
    if "cpu" not in psuComp.messages:
        psuComp.messages["cpu"] = []
    if "gpu" not in psuComp.messages:
        psuComp.messages["gpu"] = []

    cpuTDP = 0
    gpuTDP = 0

    if userBuild.components.get("cpu"):
        cpu = userBuild.components["cpu"][0]
        cpuTDPstr = cpu.specs.tdp[0]
        cpuTDP = float(cpuTDPstr.split(" ")[0])

    if userBuild.components.get("gpu"):
        gpu = userBuild.components["gpu"][0]
        gpuTDPstr = gpu.specs.tdp[0]
        gpuTDP = float(gpuTDPstr.split(" ")[0])

    psuWattageStr = psu.specs.wattage[0]
    psuWattage = float(psuWattageStr.split(" ")[0])

    totalPowerConsumption = cpuTDP + gpuTDP

    if totalPowerConsumption <= psuWattage:
        return True

    if cpuTDP > 0:
        psuComp.compatibilities["cpu"]["tdp"] = False
        psuComp.messages["cpu"].append(
            f"Incompatible CPU: The total power consumption of the CPU is {cpuTDP} W, "
            f"but the PSU provides only {psuWattage} W."
        )

    if gpuTDP > 0:
        psuComp.compatibilities["gpu"]["tdp"] = False
        psuComp.messages["gpu"].append(
            f"Incompatible GPU: The total power consumption of the GPU is {gpuTDP} W, "
            f"but the PSU provides only {psuWattage} W."
        )

    return False
