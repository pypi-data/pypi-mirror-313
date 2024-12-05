def suggestCompatiblePSUs(userBuild, psuComp):
    from pc_builder.components.psu import loadPSUsfromJSON

    def extractPrice(price_str):
        cleanPrice = price_str.replace("€", "").replace("$", "").strip()
        return float(cleanPrice)

    def getCompatiblePSUs(psus, build):
        return [psu for psu in psus if psu.checkCompatibility(build)[0]]

    allPSUs = loadPSUsfromJSON()
    compatiblePSUs = getCompatiblePSUs(allPSUs, userBuild)

    budget = userBuild.budget
    if budget == 0:
        return compatiblePSUs[:5]

    psuPercentage = 0.08  # 8% for both use cases, so no need to check
    psuBudget = budget * psuPercentage

    if userBuild.totalPrice > budget:
        lowestCostPSUs = sorted(
            compatiblePSUs,
            key=lambda psu: extractPrice(psu.price),
        )
        return lowestCostPSUs[:5]
    else:
        psusInBudget = [
            psu
            for psu in compatiblePSUs
            if extractPrice(psu.price) <= psuBudget
            and (extractPrice(psu.price) <= budget - userBuild.totalPrice)
        ]
        if not psusInBudget:
            lowestCostPSUs = sorted(
                compatiblePSUs,
                key=lambda psu: extractPrice(psu.price),
            )
            return lowestCostPSUs[:5]

        sortedPSUs = sorted(
            psusInBudget,
            key=lambda psu: extractPrice(psu.price),
            reverse=True,
        )
        return sortedPSUs[:5]
