def suggestCompatibleGPUs(userBuild, gpuComp):
    from pc_builder.components.gpu import loadGPUsfromJSON

    def extractPrice(price_str):
        cleanPrice = price_str.replace("€", "").replace("$", "").strip()
        return float(cleanPrice)

    def getCompatibleGPUs(gpus, build):
        return [gpu for gpu in gpus if gpu.checkCompatibility(build)[0]]

    allGPUs = loadGPUsfromJSON()
    compatibleGPUs = getCompatibleGPUs(allGPUs, userBuild)

    budget = userBuild.budget
    if budget == 0:
        return compatibleGPUs[:5]

    if userBuild.useCase == "work":
        gpuPercentage = 0.3  # 30%
    else:
        gpuPercentage = 0.35  # 35%

    gpuBudget = budget * gpuPercentage

    if userBuild.totalPrice > budget:
        lowestCostGPUs = sorted(
            compatibleGPUs,
            key=lambda gpu: extractPrice(gpu.price),
        )
        return lowestCostGPUs[:5]
    else:
        gpusInBudget = [
            gpu
            for gpu in compatibleGPUs
            if extractPrice(gpu.price) <= gpuBudget
            and (extractPrice(gpu.price) <= budget - userBuild.totalPrice)
        ]
        if not gpusInBudget:
            lowestCostGPUs = sorted(
                compatibleGPUs,
                key=lambda gpu: extractPrice(gpu.price),
            )
            return lowestCostGPUs[:5]

        sortedGPUs = sorted(
            gpusInBudget,
            key=lambda gpu: extractPrice(gpu.price),
            reverse=True,
        )
        return sortedGPUs[:5]
