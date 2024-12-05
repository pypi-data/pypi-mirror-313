def checkCPU_MotherboardCompatibility(cpu, userBuild, cpuComp):
    if "motherboard" not in cpuComp.messages:
        cpuComp.messages["motherboard"] = []

    if not userBuild.components.get("motherboard"):
        return True

    motherboard = userBuild.components["motherboard"][0]
    mbSocket = motherboard.specs.socket_cpu[0]
    cpuSocket = cpu.specs.socket_type[0]

    if mbSocket == cpuSocket:
        return True

    cpuComp.compatibilities["motherboard"]["socket_cpu"] = False
    cpuComp.messages["motherboard"].append(
        f"Incompatible CPU socket: '{cpuSocket}' does not match motherboard socket '{mbSocket}'."
    )
    return False


def checkCPU_CPUCoolerCompatibility(cpu, userBuild, cpuComp):
    if "cpucooler" not in cpuComp.messages:
        cpuComp.messages["cpucooler"] = []

    if not userBuild.components.get("cpucooler"):
        return True

    cpuCooler = userBuild.components["cpucooler"][0]
    cpuCoolerSockets = cpuCooler.specs.cpu_sockets
    cpuSocket = cpu.specs.socket_type[0]

    if cpuSocket in cpuCoolerSockets:
        return True

    cpuComp.compatibilities["cpucooler"]["cpu_sockets"] = False
    cpuComp.messages["cpucooler"].append(
        f"Incompatible CPU cooler: '{cpuCooler.name}' does not support CPU socket '{cpuSocket}'. "
        f"Supported sockets: {', '.join(cpuCoolerSockets)}."
    )
    return False


def checkCPU_PSUCompatibility(cpu, userBuild, cpuComp):
    if "psu" not in cpuComp.messages:
        cpuComp.messages["psu"] = []

    if not userBuild.components.get("psu"):
        return True

    psu = userBuild.components["psu"][0]
    psuWattagestr = psu.specs.wattage[0]
    psuWattage = float(psuWattagestr.split(" ")[0])
    cpuTDPstr = cpu.specs.tdp[0]
    cpuTDP = float(cpuTDPstr.split(" ")[0])

    if not userBuild.components.get("gpu"):
        if cpuTDP < psuWattage:
            return True

        cpuComp.compatibilities["psu"]["wattage"] = False
        cpuComp.messages["psu"].append(
            f"Incompatible PSU wattage: CPU TDP '{cpuTDP}W' exceeds PSU wattage '{psuWattage}W'."
        )
        return False

    gpu = userBuild.components["gpu"][0]
    gpuTDPstr = gpu.specs.tdp[0]
    gpuTDP = float(gpuTDPstr.split(" ")[0])

    if cpuTDP + gpuTDP < psuWattage:
        return True

    cpuComp.compatibilities["psu"]["wattage"] = False
    cpuComp.messages["psu"].append(
        f"Incompatible PSU wattage: Combined TDP '{cpuTDP + gpuTDP}W' exceeds PSU wattage '{psuWattage}W'."
    )
    return False
