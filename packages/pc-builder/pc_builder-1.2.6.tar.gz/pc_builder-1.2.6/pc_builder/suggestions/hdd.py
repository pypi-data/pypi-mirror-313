def suggestCompatibleHDDs(userBuild, hddComp):
    from pc_builder.components.hdd import loadHDDsfromJSON

    # Helper: Extract numerical price from string
    def extractPrice(price_str):
        cleanPrice = price_str.replace("€", "").replace("$", "").strip()
        return float(cleanPrice)  # Convert to float

    # Helper: Check compatibility
    def getCompatibleHDDs(hdds, build):
        return [hdd for hdd in hdds if hdd.checkCompatibility(build)[0]]

    allHDDs = loadHDDsfromJSON()
    compatibleHDDs = getCompatibleHDDs(allHDDs, userBuild)

    # Step 1: Handle zero-budget scenario
    budget = userBuild.budget
    if budget == 0:
        return compatibleHDDs[:5]

    # Step 2: Determine percentage of budget for storage (HDD + SSD)
    if userBuild.useCase == "work":
        storagePercentage = 0.12  # 12%
    else:
        storagePercentage = 0.10  # 10%

    # Step 3: Calculate remaining storage budget
    # Include costs of both HDD and SSD in the build
    allStorageInBuild = userBuild.components.get("hdd", []) + userBuild.components.get(
        "ssd", []
    )
    totalStorageCost = sum(extractPrice(storage.price) for storage in allStorageInBuild)
    storageBudget = budget * storagePercentage - totalStorageCost
    storageBudgetRemaining = max(storageBudget, 0)

    # Step 4: Handle out-of-budget or insufficient storage budget cases
    if userBuild.totalPrice > budget or storageBudgetRemaining == 0:
        # Out of budget or no budget for storage: return cheapest compatible HDDs
        lowestCostHDDs = sorted(compatibleHDDs, key=lambda hdd: extractPrice(hdd.price))
        return lowestCostHDDs[:5]
    else:
        # Filter HDDs within remaining storage budget and overall budget
        hddsInBudget = [
            hdd
            for hdd in compatibleHDDs
            if (extractPrice(hdd.price) <= storageBudgetRemaining)
            and (extractPrice(hdd.price) <= budget - userBuild.totalPrice)
        ]

        # If no HDDs are within budget, return cheapest compatible HDDs
        if not hddsInBudget:
            lowestCostHDDs = sorted(
                compatibleHDDs, key=lambda hdd: extractPrice(hdd.price)
            )
            return lowestCostHDDs[:5]

        # Sort HDDs within budget by price descending, return top 5
        sortedHDDs = sorted(
            hddsInBudget, key=lambda hdd: extractPrice(hdd.price), reverse=True
        )
        return sortedHDDs[:5]
