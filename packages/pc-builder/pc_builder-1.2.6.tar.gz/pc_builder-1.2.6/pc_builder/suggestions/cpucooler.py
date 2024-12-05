def suggestCompatibleCPUcoolers(userBuild, cpuCoolerComp):
    from pc_builder.components.cpucooler import loadCPUCoolersfromJSON

    # Helper: Extract numerical price from string
    def extractPrice(price_str):
        cleanPrice = price_str.replace("€", "").replace("$", "").strip()
        return float(cleanPrice)

    # Helper: Get compatible CPU coolers
    def getCompatibleCoolers(coolers, build):
        return [cooler for cooler in coolers if cooler.checkCompatibility(build)[0]]

    allCoolers = loadCPUCoolersfromJSON()
    compatibleCoolers = getCompatibleCoolers(allCoolers, userBuild)

    # Step 1: Handle zero-budget scenario
    budget = userBuild.budget
    if budget == 0:
        return compatibleCoolers[:5]

    # Step 2: Determine percentage of budget for the CPU cooler
    if userBuild.useCase == "work":
        coolingPercentage = 0.05  # 5%
    else:
        coolingPercentage = 0.04  # 4%

    # Step 3: Calculate the CPU cooler budget
    coolingBudget = budget * coolingPercentage

    # Step 4: Handle out-of-budget or insufficient CPU cooler budget scenarios
    if userBuild.totalPrice > budget:
        # Out of budget or no budget for CPU coolers: return cheapest compatible coolers
        lowestCostCoolers = sorted(
            compatibleCoolers, key=lambda cooler: extractPrice(cooler.price)
        )
        return lowestCostCoolers[:5]
    else:
        # Filter coolers within the calculated CPU cooler budget
        coolersInBudget = [
            cooler
            for cooler in compatibleCoolers
            if extractPrice(cooler.price) <= coolingBudget
            and (extractPrice(cooler.price) <= budget - userBuild.totalPrice)
        ]

        # If no coolers are within budget, return cheapest compatible coolers
        if not coolersInBudget:
            lowestCostCoolers = sorted(
                compatibleCoolers, key=lambda cooler: extractPrice(cooler.price)
            )
            return lowestCostCoolers[:5]

        # Sort coolers within budget by price descending, return top 5
        sortedCoolers = sorted(
            coolersInBudget, key=lambda cooler: extractPrice(cooler.price), reverse=True
        )
        return sortedCoolers[:5]
