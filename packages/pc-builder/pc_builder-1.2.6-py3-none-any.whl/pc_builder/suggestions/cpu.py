def suggestCompatibleCPUs(userBuild, cpuComp):
    from pc_builder.components.cpu import loadCPUsfromJSON

    # Helper: Extract numerical price from string
    def extractPrice(price_str):
        cleanPrice = price_str.replace("€", "").replace("$", "").strip()
        return float(cleanPrice)

    # Helper: Get compatible CPUs
    def getCompatibleCPUs(cpus, build):
        return [cpu for cpu in cpus if cpu.checkCompatibility(build)[0]]

    allCPUs = loadCPUsfromJSON()
    compatibleCPUs = getCompatibleCPUs(allCPUs, userBuild)

    # Step 1: Handle zero-budget scenario
    budget = userBuild.budget
    if budget == 0:
        return compatibleCPUs[:5]

    # Step 2: Determine percentage of budget for the CPU
    # Both gaming and work allocate 20% of the budget to the CPU
    cpuPercentage = 0.2

    # Step 3: Calculate the CPU budget
    cpuBudget = budget * cpuPercentage

    # Step 4: Handle out-of-budget or insufficient CPU budget scenarios
    if userBuild.totalPrice > budget:
        # Out of budget or no budget for CPUs: return cheapest compatible CPUs
        lowestCostCPUs = sorted(compatibleCPUs, key=lambda cpu: extractPrice(cpu.price))
        return lowestCostCPUs[:5]
    else:
        # Filter CPUs within the calculated CPU budget
        cpusInBudget = [
            cpu
            for cpu in compatibleCPUs
            if extractPrice(cpu.price) <= cpuBudget
            and (extractPrice(cpu.price) <= budget - userBuild.totalPrice)
        ]

        # If no CPUs are within budget, return cheapest compatible CPUs
        if not cpusInBudget:
            lowestCostCPUs = sorted(
                compatibleCPUs, key=lambda cpu: extractPrice(cpu.price)
            )
            return lowestCostCPUs[:5]

        # Sort CPUs within budget by performance (or price descending), return top 5
        sortedCPUs = sorted(
            cpusInBudget, key=lambda cpu: extractPrice(cpu.price), reverse=True
        )
        return sortedCPUs[:5]
