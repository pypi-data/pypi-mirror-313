def checkCPUCooler_CPUCompatibility(cpuCooler, userBuild, cpuCoolerComp):
    if "cpu" not in cpuCoolerComp.messages:
        cpuCoolerComp.messages["cpu"] = []

    if not userBuild.components.get("cpu"):
        return True

    cpu = userBuild.components["cpu"][0]
    cpuSocketType = cpu.specs.socket_type[0]

    if cpuSocketType in cpuCooler.specs.cpu_sockets:
        return True

    cpuCoolerComp.compatibilities["cpu"]["socket"] = False
    cpuCoolerComp.messages["cpu"].append(
        f"Incompatible CPU cooler: '{cpuCooler.name}' does not support CPU socket '{cpuSocketType}'. "
        f"Supported sockets: {', '.join(cpuCooler.specs.cpu_sockets)}."
    )
    return False
