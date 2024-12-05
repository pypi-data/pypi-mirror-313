def suggestCompatibleSSDs(userBuild, ssdComp):
    from pc_builder.components.ssd import loadSSDsfromJSON

    # Helper: Extract numerical price from string
    def extractPrice(price_str):
        cleanPrice = price_str.replace("€", "").replace("$", "").strip()
        return float(cleanPrice)  # Convert to float

    # Helper: Check compatibility
    def getCompatibleSSDs(ssds, build, ssdType):
        if ssdType == "any":
            return [ssd for ssd in ssds if ssd.checkCompatibility(build)[0]]
        return [
            ssd
            for ssd in ssds
            if ssd.checkCompatibility(build)[0]
            and any(ssdType in interface for interface in ssd.specs.interface)
        ]

    allSSDs = loadSSDsfromJSON()
    if (
        userBuild.selectedPart
        and hasattr(userBuild.selectedPart, "specs")
        and hasattr(userBuild.selectedPart.specs, "interface")
    ):
        ssdType = (
            "M.2"
            if any(
                "M.2" in interface
                for interface in userBuild.selectedPart.specs.interface
            )
            else "SATA"
        )
    else:
        ssdType = "any"

    compatibleSSDs = getCompatibleSSDs(allSSDs, userBuild, ssdType)

    # Step 1: Handle zero-budget scenario
    budget = userBuild.budget
    if budget == 0:
        return compatibleSSDs[:5]

    # Step 2: Determine percentage of budget for storage (SSD + SSD)
    if userBuild.useCase == "work":
        storagePercentage = 0.12  # 12%
    else:
        storagePercentage = 0.10  # 10%

    # Step 3: Calculate remaining storage budget
    # Include costs of both SSD and SSD in the build
    allStorageInBuild = userBuild.components.get("hdd", []) + userBuild.components.get(
        "ssd", []
    )
    totalStorageCost = sum(extractPrice(storage.price) for storage in allStorageInBuild)
    storageBudget = budget * storagePercentage - totalStorageCost
    storageBudgetRemaining = max(storageBudget, 0)

    # Step 4: Handle out-of-budget or insufficient storage budget cases
    if userBuild.totalPrice > budget or storageBudgetRemaining == 0:
        # Out of budget or no budget for storage: return cheapest compatible SSDs
        lowestCostSSDs = sorted(compatibleSSDs, key=lambda ssd: extractPrice(ssd.price))
        return lowestCostSSDs[:5]
    else:
        # Filter SSDs within remaining storage budget and overall budget
        SSDsInBudget = [
            ssd
            for ssd in compatibleSSDs
            if (extractPrice(ssd.price) <= storageBudgetRemaining)
            and (extractPrice(ssd.price) <= budget - userBuild.totalPrice)
        ]

        # If no SSDs are within budget, return cheapest compatible SSDs
        if not SSDsInBudget:
            lowestCostSSDs = sorted(
                compatibleSSDs, key=lambda ssd: extractPrice(ssd.price)
            )
            return lowestCostSSDs[:5]

        # Sort SSDs within budget by price descending, return top 5
        sortedSSDs = sorted(
            SSDsInBudget, key=lambda ssd: extractPrice(ssd.price), reverse=True
        )
        return sortedSSDs[:5]
