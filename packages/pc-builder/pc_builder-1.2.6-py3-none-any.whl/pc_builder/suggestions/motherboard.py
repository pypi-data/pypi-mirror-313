def suggestCompatibleMotherboards(userBuild, motherboardComp):
    from pc_builder.components.motherboard import loadMBsfromJSON

    def extractPrice(price_str):
        cleanPrice = price_str.replace("€", "").replace("$", "").strip()
        return float(cleanPrice)

    def getCompatibleMotherboards(motherboards, build):
        return [
            motherboard
            for motherboard in motherboards
            if motherboard.checkCompatibility(build)[0]
        ]

    allMotherboards = loadMBsfromJSON()
    compatibleMotherboards = getCompatibleMotherboards(allMotherboards, userBuild)

    budget = userBuild.budget
    if budget == 0:
        return compatibleMotherboards[:5]

    motherboardPercentage = 0.1  # 10% for both use cases, so no need to check
    motherboardBudget = budget * motherboardPercentage

    if userBuild.totalPrice > budget:
        lowestCostMotherboards = sorted(
            compatibleMotherboards,
            key=lambda motherboard: extractPrice(motherboard.price),
        )
        return lowestCostMotherboards[:5]
    else:
        motherboardsInBudget = [
            motherboard
            for motherboard in compatibleMotherboards
            if extractPrice(motherboard.price) <= motherboardBudget
            and (extractPrice(motherboard.price) <= budget - userBuild.totalPrice)
        ]
        if not motherboardsInBudget:
            lowestCostMotherboards = sorted(
                compatibleMotherboards,
                key=lambda motherboard: extractPrice(motherboard.price),
            )
            return lowestCostMotherboards[:5]

        sortedMotherboards = sorted(
            motherboardsInBudget,
            key=lambda motherboard: extractPrice(motherboard.price),
            reverse=True,
        )
        return sortedMotherboards[:5]
