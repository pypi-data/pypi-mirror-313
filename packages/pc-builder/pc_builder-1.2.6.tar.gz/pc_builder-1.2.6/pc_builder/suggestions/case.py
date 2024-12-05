def suggestCompatibleCases(userBuild, caseComp):
    from pc_builder.components.case import loadCasesfromJSON

    # Helper: Extract numerical price from string
    def extractPrice(price_str):
        cleanPrice = price_str.replace("€", "").replace("$", "").strip()
        return float(cleanPrice)

    # Helper: Check compatibility
    def getCompatibleCases(cases, build):
        return [case for case in cases if case.checkCompatibility(build)[0]]

    allCases = loadCasesfromJSON()
    compatibleCases = getCompatibleCases(allCases, userBuild)

    # Step 1: Handle zero-budget scenario
    budget = userBuild.budget
    if budget == 0:
        return compatibleCases[:5]

    # Step 2: Determine percentage of budget for the case
    casePercentage = 0.05

    # Step 3: Calculate the case budget (directly, since no case exists in userBuild)
    caseBudget = budget * casePercentage

    # Step 4: Handle out-of-budget or insufficient case budget scenarios
    if userBuild.totalPrice > budget:
        # Out of budget or no budget for cases: return cheapest compatible cases
        lowestCostCases = sorted(
            compatibleCases, key=lambda case: extractPrice(case.price)
        )
        return lowestCostCases[:5]
    else:
        # Filter cases within the calculated case budget
        casesInBudget = [
            case
            for case in compatibleCases
            if extractPrice(case.price) <= caseBudget
            and (extractPrice(case.price) <= budget - userBuild.totalPrice)
        ]

        # If no cases are within budget, return cheapest compatible cases
        if not casesInBudget:
            lowestCostCases = sorted(
                compatibleCases, key=lambda case: extractPrice(case.price)
            )
            return lowestCostCases[:5]

        # Sort cases within budget by price descending, return top 5
        sortedCases = sorted(
            casesInBudget, key=lambda case: extractPrice(case.price), reverse=True
        )
        return sortedCases[:5]
