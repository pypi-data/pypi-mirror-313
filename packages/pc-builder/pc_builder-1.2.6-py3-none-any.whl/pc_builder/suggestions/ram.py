def suggestCompatibleRAMs(userBuild, ramComp):
    from pc_builder.components.ram import loadRAMsfromJSON

    # Helper: Extract numerical price from string
    def extractPrice(price_str):
        # Remove common currency symbols and strip whitespace
        cleanPrice = price_str.replace("€", "").replace("$", "").strip()
        return float(cleanPrice)  # Convert to float

    # Helper: Check compatibility
    def getCompatibleRAMs(rams, build):
        return [ram for ram in rams if ram.checkCompatibility(build)[0]]

    allRAMs = loadRAMsfromJSON()
    compatibleRAMs = getCompatibleRAMs(allRAMs, userBuild)

    # Step 1: Handle zero-budget scenario
    budget = userBuild.budget
    if budget == 0:
        return compatibleRAMs[:5]

    # Step 2: Determine percentage of budget for RAM
    if userBuild.useCase == "work":
        ramPercentage = 0.1  # 10%
    else:
        ramPercentage = 0.08  # 8%

    # Step 3: Calculate remaining RAM budget
    allRAMsInBuild = userBuild.components.get("ram", [])
    totalRAMCost = sum(extractPrice(ram.price) for ram in allRAMsInBuild)
    ramBudget = budget * ramPercentage - totalRAMCost
    ramBudgetRemaining = max(ramBudget, 0)

    # Step 4: Handle out-of-budget or insufficient RAM budget cases
    if userBuild.totalPrice > budget or ramBudgetRemaining == 0:
        # Out of budget or no budget for RAMs: return cheapest compatible RAMs
        lowestCostRAMs = sorted(compatibleRAMs, key=lambda ram: extractPrice(ram.price))
        return lowestCostRAMs[:5]
    else:
        # Filter RAMs within remaining RAM budget and remaining budget in itself
        ramsInBudget = [
            ram
            for ram in compatibleRAMs
            if (extractPrice(ram.price) <= ramBudgetRemaining)
            and (extractPrice(ram.price) <= budget - userBuild.totalPrice)
        ]

        # If no RAMs are within budget, return cheapest compatible RAMs
        if not ramsInBudget:
            lowestCostRAMs = sorted(
                compatibleRAMs, key=lambda ram: extractPrice(ram.price)
            )
            return lowestCostRAMs[:5]

        # Sort RAMs within budget by price descending, return top 5
        sortedRAMs = sorted(
            ramsInBudget, key=lambda ram: extractPrice(ram.price), reverse=True
        )
        return sortedRAMs[:5]
