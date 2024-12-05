import os
import typer
import sys
from pc_builder.components.gpu import loadGPUsfromJSON
from pc_builder.components.psu import loadPSUsfromJSON
from pc_builder.components.motherboard import loadMBsfromJSON
from pc_builder.components.cpu import loadCPUsfromJSON
from pc_builder.components.cpucooler import loadCPUCoolersfromJSON
from pc_builder.components.ram import loadRAMsfromJSON
from pc_builder.components.ssd import loadSSDsfromJSON
from pc_builder.components.hdd import loadHDDsfromJSON
from pc_builder.components.case import loadCasesfromJSON
from pc_builder.suggestions.cpu import suggestCompatibleCPUs
from pc_builder.suggestions.cpucooler import suggestCompatibleCPUcoolers
from pc_builder.suggestions.gpu import suggestCompatibleGPUs
from pc_builder.suggestions.motherboard import suggestCompatibleMotherboards
from pc_builder.suggestions.psu import suggestCompatiblePSUs
from pc_builder.suggestions.case import suggestCompatibleCases
from pc_builder.suggestions.ram import suggestCompatibleRAMs
from pc_builder.suggestions.ssd import suggestCompatibleSSDs
from pc_builder.suggestions.hdd import suggestCompatibleHDDs


def clearScreen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


app = typer.Typer()


class UserPC:
    def __init__(self):
        self.components = {
            "gpu": [],
            "psu": [],
            "motherboard": [],
            "cpu": [],
            "cpucooler": [],
            "ram": [],
            "ssd": [],
            "hdd": [],
            "case": [],
        }
        self.totalPrice = 0.0
        self.budget = 0.0
        self.useCase = None
        self.selectedPart = []

    def addComponent(self, componentType, part):
        price = float(part.price.replace("€", "").replace("$", "").strip())
        self.components[componentType].append(part)
        self.totalPrice += price

    def removeComponent(self, componentType, index):
        if componentType in self.components and index < len(
            self.components[componentType]
        ):
            price = float(
                self.components[componentType][index]
                .price.replace("€", "")
                .replace("$", "")
                .strip()
            )
            self.totalPrice -= price
            del self.components[componentType][index]

    def display(self):
        # Define the order of components to be displayed
        displayOrder = [
            "gpu",
            "cpu",
            "cpucooler",
            "motherboard",
            "case",
            "psu",
        ]

        # Display the components in the defined order
        for componentType in displayOrder:
            if self.components[componentType]:
                for part in self.components[componentType]:
                    typer.echo(
                        f"{componentType.upper()}: {cleanName(part.name)} - {part.price}"
                    )

        # Display the MEMORY section
        ramParts = self.components["ram"]
        if ramParts:
            typer.echo(typer.style("\n--- MEMORY ---", fg=typer.colors.YELLOW))
            for part in ramParts:
                typer.echo(f"RAM: {cleanName(part.name)} - {part.price}")

        # Display the STORAGE section
        ssdParts = self.components["ssd"]
        hddParts = self.components["hdd"]
        if ssdParts or hddParts:
            typer.echo(typer.style("\n--- STORAGE ---", fg=typer.colors.YELLOW))
            for part in ssdParts:
                typer.echo(f"SSD: {cleanName(part.name)} - {part.price}")
            typer.echo("---------------")
            for part in hddParts:
                typer.echo(f"HDD: {cleanName(part.name)} - {part.price}")

        # Display the total price
        typer.echo(
            typer.style(
                f"\n--- PRICE ---\nTotal Price: €{self.totalPrice:.2f}",
                fg=typer.colors.BLUE,
            )
        )


userPC = UserPC()


@app.command()
def main():
    clearScreen()
    """Welcome to the PC Builder App"""
    typer.echo(typer.style("Welcome to the PC Builder App", fg=typer.colors.YELLOW))
    start()


def start():
    clearScreen()
    """Main Menu"""
    while True:
        # Display user preferences
        typer.echo(typer.style("\n--- Current Preferences ---", fg=typer.colors.YELLOW))
        if userPC.budget:
            typer.echo(f"Budget: €{userPC.budget:.2f}")
        else:
            typer.echo("Budget: Not Set")

        if userPC.useCase:
            typer.echo(f"Use Case: {userPC.useCase.capitalize()}")
        else:
            typer.echo("Use Case: Not Set")

        typer.echo(typer.style("\n--- Main Menu ---", fg=typer.colors.YELLOW))

        # Menu options with dynamic numbering
        option_number = 1
        options = {}

        # Option 1: Add components
        typer.echo(
            typer.style(f"{option_number}) Add components", fg=typer.colors.CYAN)
        )
        options[option_number] = chooseComponent
        option_number += 1

        # Option 2: View purchase
        typer.echo(typer.style(f"{option_number}) View purchase", fg=typer.colors.CYAN))
        options[option_number] = viewPurchase
        option_number += 1

        # Option 3: Set user preferences
        typer.echo(
            typer.style(f"{option_number}) Set user preferences", fg=typer.colors.CYAN)
        )
        options[option_number] = setPreferences
        option_number += 1

        # Option 4: Show suggested build (conditionally displayed)
        manuallyAddedParts = any(
            userPC.components[component] for component in userPC.components
        )
        if userPC.budget and userPC.useCase and not manuallyAddedParts:
            typer.echo(
                typer.style(
                    f"{option_number}) Show full suggested build",
                    fg=typer.colors.BRIGHT_GREEN,
                )
            )
            options[option_number] = showSuggestedBuild
            option_number += 1

        # Options for builds with manually added parts
        if manuallyAddedParts:
            typer.echo(
                typer.style(f"{option_number}) Remove component", fg=typer.colors.RED)
            )
            options[option_number] = removeComponent
            option_number += 1

            typer.echo(
                typer.style(f"{option_number}) Finish build", fg=typer.colors.GREEN)
            )
            options[option_number] = finishBuild
            option_number += 1

        # Option for exit
        typer.echo(typer.style(f"{option_number}) Exit", fg=typer.colors.BRIGHT_RED))
        options[option_number] = exitApp

        # Get user choice
        choice = typer.prompt("Choose an option", type=int)

        # Execute selected option
        if choice in options:
            options[choice]()
        else:
            typer.echo(
                typer.style("Invalid choice, please try again.", fg=typer.colors.RED)
            )
            clearScreen()


def exitApp():
    """Exit the application."""
    typer.echo(
        typer.style("Thank you for using the PC Builder App!", fg=typer.colors.GREEN)
    )
    sys.exit()


def setPreferences():
    clearScreen()
    """Set preferences for your PC build."""
    while True:
        typer.echo(
            typer.style("\n--- Set User Preferences ---", fg=typer.colors.YELLOW)
        )
        typer.echo(typer.style("1) Set Budget", fg=typer.colors.CYAN))
        typer.echo(typer.style("2) Set Use Case", fg=typer.colors.CYAN))
        typer.echo(typer.style("3) Back to Main Menu", fg=typer.colors.BRIGHT_RED))

        choice = typer.prompt("Choose an option", type=int)

        if choice == 1:
            setBudget()
        elif choice == 2:
            setUseCase()
        elif choice == 3:
            clearScreen()
            return
        else:
            typer.echo(
                typer.style("Invalid choice, please try again.", fg=typer.colors.RED)
            )
            clearScreen()


def setBudget():
    while True:
        budget = typer.prompt("Enter your budget (in €)", type=float)
        if budget < 500:
            typer.echo(
                typer.style(
                    "Error: Budget cannot be less than €500. Please enter a higher amount.",
                    fg=typer.colors.RED,
                )
            )
        else:
            userPC.budget = budget
            typer.echo(
                typer.style(
                    f"Budget set to €{userPC.budget:.2f}", fg=typer.colors.GREEN
                )
            )
            break


def setUseCase():
    useCases = ["gaming", "work"]
    typer.echo(typer.style("\nSelect your primary use case:", fg=typer.colors.YELLOW))
    for idx, useCase in enumerate(useCases, start=1):
        typer.echo(f"{idx}) {useCase.capitalize()}")

    choice = typer.prompt("Enter the number corresponding to your use case", type=int)
    if 1 <= choice <= len(useCases):
        userPC.useCase = useCases[choice - 1]
        typer.echo(
            typer.style(
                f"Use case set to {userPC.useCase.capitalize()}", fg=typer.colors.GREEN
            )
        )
    else:
        typer.echo(
            typer.style("Invalid choice. Use case not set.", fg=typer.colors.RED)
        )


def showSuggestedBuild():
    clearScreen()
    typer.echo(typer.style("\n--- Suggested Build ---", fg=typer.colors.YELLOW))

    if not userPC.budget or not userPC.useCase:
        typer.echo(
            typer.style("Error: Set budget and use case first.", fg=typer.colors.RED)
        )
        return

    # Initialize total price
    totalPrice = 0.0

    # Define all components to be added
    components = [
        ("motherboard", suggestCompatibleMotherboards),
        ("cpu", suggestCompatibleCPUs),
        ("cpucooler", suggestCompatibleCPUcoolers),
        ("gpu", suggestCompatibleGPUs),
        ("psu", suggestCompatiblePSUs),
        ("ram", suggestCompatibleRAMs),
        ("ssd", suggestCompatibleSSDs),
        ("case", suggestCompatibleCases),
    ]

    # Dictionary to store suggested components
    suggestedComponents = {}

    for component, suggestFunction in components:
        # Suggest compatible components
        suggestedItems = suggestFunction(userPC, None)

        if not suggestedItems:
            typer.echo(
                typer.style(
                    f"No compatible {component} found within the budget.",
                    fg=typer.colors.RED,
                )
            )
            return

        # Select the first (most compatible and affordable) component
        suggestedItem = suggestedItems[0]
        itemPrice = float(suggestedItem.price.replace("€", "").strip())

        # Add to total price and store suggestion
        totalPrice += itemPrice
        suggestedComponents[component] = suggestedItem

        # Display the suggested component
        typer.echo(
            f"{component.capitalize()}: {cleanName(suggestedItem.name)} - €{itemPrice:.2f}"
        )

    typer.echo(typer.style(f"\nTotal Price: €{totalPrice:.2f}", fg=typer.colors.BLUE))

    # Prompt user to finalize or discard the build
    confirm = typer.prompt(
        "Do you want to finalize this build with the suggested components? (y/n)",
        type=str,
    )
    if confirm.lower() == "y":
        for component, suggestedItem in suggestedComponents.items():
            userPC.addComponent(component, suggestedItem)
        typer.echo(
            typer.style("All components added to your build!", fg=typer.colors.GREEN)
        )
    else:
        typer.echo(
            typer.style(
                "Build not finalized. You can manually add components or try again.",
                fg=typer.colors.RED,
            )
        )


def chooseComponent():
    clearScreen()
    """Select and add components to your build."""
    while True:
        typer.echo(typer.style("\n--- Choose a Component ---", fg=typer.colors.YELLOW))
        typer.echo("1) GPU")
        typer.echo("2) PSU")
        typer.echo("3) Motherboard")
        typer.echo("4) CPU")
        typer.echo("5) CPU cooler")
        typer.echo("6) RAM")
        typer.echo("7) SSD")
        typer.echo("8) HDD")
        typer.echo("9) Case")
        typer.echo(typer.style("10) Back to Main Menu", fg=typer.colors.CYAN))

        choice = typer.prompt("Choose a component to add", type=int)

        if choice == 1:
            clearScreen()
            selectComponent("gpu")
        elif choice == 2:
            clearScreen()
            selectComponent("psu")
        elif choice == 3:
            clearScreen()
            selectComponent("motherboard")
        elif choice == 4:
            clearScreen()
            selectComponent("cpu")
        elif choice == 5:
            clearScreen()
            selectComponent("cpucooler")
        elif choice == 6:
            clearScreen()
            selectComponent("ram")
        elif choice == 7:
            clearScreen()
            selectComponent("ssd")
        elif choice == 8:
            clearScreen()
            selectComponent("hdd")
        elif choice == 9:
            clearScreen()
            selectComponent("case")
        elif choice == 10:
            clearScreen()
            return  # Return to Main Menu
        else:
            typer.echo(
                typer.style("Invalid choice, please try again.", fg=typer.colors.RED)
            )
            clearScreen()


def formatSpecifications(specs):
    """Format the specifications of a part for better readability."""
    typer.echo(typer.style("\nFull Specifications:", fg=typer.colors.YELLOW))

    # Iterate over each specification and print in readable format
    for key, value in specs.items():
        # Skip none or empty values
        if value is None or value == "":
            continue

        # If the value is a list, join non-None values
        if isinstance(value, list):
            readableValue = ", ".join(
                [str(v) for v in value if v is not None and v != ""]
            )
        else:
            readableValue = str(value)

        # Print only if there is a valid value
        if readableValue:
            print(f"{key.replace('_', ' ').capitalize()}: {readableValue}")


def cleanName(name):
    """Remove text within the last set of parentheses and any redundant repeating words in the component name."""
    # Find the last opening parenthesis
    lastOpen = name.rfind("(")
    if lastOpen != -1:
        # Remove the text in the last parentheses and the parentheses themselves
        name = name[:lastOpen].strip()

    words = name.split()
    uniqueWords = []
    if "Memory" in name:
        seenWords = set()
        for word in words:
            if (word, len(uniqueWords)) not in seenWords:
                uniqueWords.append(word)
                seenWords.add((word, len(uniqueWords)))
        return " ".join(uniqueWords)

    for word in words:
        if word not in uniqueWords:
            uniqueWords.append(word)
    return " ".join(uniqueWords)


def ramLimitCheck(componentType, selectedPart):
    ramLimit = 4
    ramAmount = 0

    for stick in userPC.components["ram"]:
        stickStr = stick.specs.modules[0]
        stickAmount, _ = stickStr.split(" x ")
        stickAmount = int(stickAmount)
        ramAmount += stickAmount

    if ramAmount == ramLimit:
        typer.echo(
            typer.style(
                f"Error: You have reached a {componentType.upper()} limit. There are no motherboards that support more than 4 RAM sticks",
                fg=typer.colors.RED,
            )
        )
        return False

    if selectedPart:
        stick = selectedPart
        stickStr = stick.specs.modules[0]
        stickAmount, _ = stickStr.split(" x ")
        stickAmount = int(stickAmount)
        ramAmount += stickAmount

    if ramAmount > ramLimit:
        typer.echo(
            typer.style(
                f"Error: You have reached a {componentType.upper()} limit. There are no motherboards that support more than 4 RAM sticks",
                fg=typer.colors.RED,
            )
        )
        return False

    return True


def selectComponent(componentType):
    """Select a component from available options with pagination, intelligent suggestions, and sorting options."""
    userPC.selectedPart = []
    noLimitParts = ["ram", "hdd", "ssd"]

    # Check if this component type already exists in the user's build
    if componentType not in noLimitParts and userPC.components[componentType]:
        typer.echo(
            typer.style(
                f"Error: You already have a {componentType.upper()} in your build. Remove it first to add a new one.",
                fg=typer.colors.RED,
            )
        )
        return  # Exit to the component menu

    # RAM-specific limit check
    if componentType == "ram" and not ramLimitCheck(componentType, None):
        return

    # Load available parts
    parts = getComponents(componentType)
    if not parts:
        typer.echo(
            typer.style(
                f"No {componentType.upper()} components available.", fg=typer.colors.RED
            )
        )
        return

    # Sorting setup
    sortCriteria = "name"  # Default sort criteria: name
    sortOrder = "asc"  # Default sort order: ascending
    active_price_range = {"min": None, "max": None}  # Default price range
    min_price = None
    max_price = None
    search_term = None

    # Check if a part is within the active price range
    def within_price_range(part):
        price = float(part.price.replace("€", "").replace("$", "").strip())
        return (
            active_price_range["min"] is None or price >= active_price_range["min"]
        ) and (active_price_range["max"] is None or price <= active_price_range["max"])

    # Apply sorting and filtering to the parts list
    def applyFiltersAndSorting(parts):
        # Apply search filter
        filtered_parts = parts
        if search_term:
            filtered_parts = filter(
                lambda part: search_term in cleanName(part.name).lower(), filtered_parts
            )
        # Apply price range filter
        if active_price_range["min"] or active_price_range["max"]:
            filtered_parts = filter(within_price_range, filtered_parts)
        # Apply sorting
        return applySorting(list(filtered_parts))

    # Apply sorting based on the criteria and order
    def applySorting(parts):
        if sortCriteria == "name":
            return sorted(
                parts,
                key=lambda p: cleanName(p.name).lower(),
                reverse=(sortOrder == "desc"),
            )
        elif sortCriteria == "price":
            return sorted(
                parts,
                key=lambda p: float(p.price.replace("€", "").replace("$", "").strip()),
                reverse=(sortOrder == "desc"),
            )

    sortedParts = applyFiltersAndSorting(parts)

    # Pagination setup
    pageSize = 10
    totalParts = len(sortedParts)
    totalPages = (totalParts + pageSize - 1) // pageSize
    currentPage = 0

    # Suggestion function mapping
    suggestionFunctions = {
        "gpu": suggestCompatibleGPUs,
        "psu": suggestCompatiblePSUs,
        "motherboard": suggestCompatibleMotherboards,
        "cpu": suggestCompatibleCPUs,
        "cpucooler": suggestCompatibleCPUcoolers,
        "ram": suggestCompatibleRAMs,
        "ssd": suggestCompatibleSSDs,
        "hdd": suggestCompatibleHDDs,
        "case": suggestCompatibleCases,
    }
    suggestFunc = suggestionFunctions.get(componentType)

    while True:
        # Display current page of parts
        startIdx = currentPage * pageSize
        endIdx = min(startIdx + pageSize, totalParts)

        clearScreen()
        typer.echo(
            typer.style(
                f"\n--- {componentType.upper()} Selection (Page {currentPage + 1}/{totalPages}) ---",
                fg=typer.colors.YELLOW,
            )
        )

        for i, part in enumerate(sortedParts[startIdx:endIdx], start=1):
            typer.echo(f"{i}) {cleanName(part.name)} - {part.price}")

        # Intelligent suggestions option
        intelligentSuggestionsOption = None
        if userPC.budget and userPC.useCase and suggestFunc:
            intelligentSuggestionsOption = pageSize + 1
            typer.echo(
                typer.style(
                    f"{intelligentSuggestionsOption}) View Intelligent Suggestions",
                    fg=typer.colors.BRIGHT_GREEN,
                )
            )

        # Navigation and sorting options
        typer.echo(
            typer.style(
                f"{pageSize + 2}) Sorting Options", fg=typer.colors.BRIGHT_MAGENTA
            )
        )
        if currentPage < totalPages - 1:
            typer.echo(typer.style(f"{pageSize + 3}) Next Page", fg=typer.colors.BLUE))
        if currentPage > 0:
            typer.echo(
                typer.style(f"{pageSize + 4}) Previous Page", fg=typer.colors.MAGENTA)
            )
        typer.echo(
            typer.style(f"{pageSize + 5}) Exit to Component Menu", fg=typer.colors.RED)
        )

        # Get user's choice
        try:
            choice = typer.prompt("Choose a component or navigate pages", type=int)
        except ValueError:
            typer.echo(
                typer.style(
                    "Invalid input. Please enter a number.", fg=typer.colors.RED
                )
            )
            continue

        # Handle part selection
        if 1 <= choice <= pageSize and (startIdx + choice - 1) < totalParts:
            userPC.selectedPart = selectedPart = sortedParts[startIdx + choice - 1]
            typer.echo(
                typer.style(
                    f"Checking compatibility for {cleanName(selectedPart.name)}...",
                    fg=typer.colors.YELLOW,
                )
            )
            isCompatible, compatibilityDetails = selectedPart.checkCompatibility(userPC)

            # Handle incompatibility
            if not isCompatible:
                typer.echo(
                    typer.style(
                        "This part is not compatible with your current build.",
                        fg=typer.colors.RED,
                    )
                )
                displayIncompatibilityMessages(
                    compatibilityDetails, componentType, userPC
                )
                return

            # Handle compatible part
            typer.echo(
                typer.style(
                    f"\nYou selected {cleanName(userPC.selectedPart.name)} for {userPC.selectedPart.price}",
                    fg=typer.colors.GREEN,
                )
            )
            formatSpecifications(userPC.selectedPart.specs.to_dict())
            confirmChoice = typer.prompt(
                "Do you want to add this to your build? (y/n)", type=str
            )
            if confirmChoice.lower() == "y":
                userPC.addComponent(componentType, userPC.selectedPart)
                typer.echo(
                    typer.style(
                        f"{componentType.upper()} added to your build.",
                        fg=typer.colors.GREEN,
                    )
                )
                return  # Exit to component menu
            else:
                typer.echo(
                    typer.style(
                        "Selection cancelled. Returning to menu.",
                        fg=typer.colors.RED,
                    )
                )
                return

        # Handle "View Intelligent Suggestions"
        elif intelligentSuggestionsOption and choice == intelligentSuggestionsOption:
            if not suggestFunc:
                typer.echo(
                    typer.style(
                        f"No suggestion function available for {componentType.upper()}.",
                        fg=typer.colors.RED,
                    )
                )
                continue
            suggestComponent(userPC, componentType, None)
            return  # Exit to general component menu after suggestions

        # Handle "Sorting Options"
        elif choice == pageSize + 2:
            while True:
                typer.echo(
                    typer.style(
                        "\n--- Sorting Options ---", fg=typer.colors.BRIGHT_MAGENTA
                    )
                )
                # Display current sorting criteria and order
                if active_price_range["min"] or active_price_range["max"]:
                    min_display = (
                        f"€{active_price_range['min']:.2f}"
                        if active_price_range["min"]
                        else "No Min"
                    )
                    max_display = (
                        f"€{active_price_range['max']:.2f}"
                        if active_price_range["max"]
                        else "No Max"
                    )
                    typer.echo(
                        typer.style(
                            f"Current Price Range: {min_display} - {max_display}",
                            fg=typer.colors.BRIGHT_BLUE,
                        )
                    )
                else:
                    typer.echo(
                        typer.style("No price range set.", fg=typer.colors.YELLOW)
                    )
                currentSorting = f"Sorting by {sortCriteria.capitalize()} ({'Ascending' if sortOrder == 'asc' else 'Descending'})"
                typer.echo(
                    typer.style(
                        f"Current sorting: {currentSorting}", fg=typer.colors.YELLOW
                    )
                )

                # Display the active keyword, if any
                if "search_term" in locals() and search_term:
                    typer.echo(
                        typer.style(
                            f"Active Keyword: '{search_term}'",
                            fg=typer.colors.BRIGHT_GREEN,
                        )
                    )
                else:
                    typer.echo(typer.style("No keyword set.", fg=typer.colors.YELLOW))

                # Determine next order for Name and Price sorting
                if sortCriteria == "name":
                    nextNameOrder = "Z-A" if sortOrder == "asc" else "A-Z"
                    nextPriceOrder = "Ascending"  # Price order should not be toggled when sorting by Name
                else:
                    nextNameOrder = (
                        "A-Z"  # Name order should not be toggled when sorting by Price
                    )
                    nextPriceOrder = "Descending" if sortOrder == "asc" else "Ascending"

                # Show sorting options
                typer.echo(f"1) Sort by Name ({nextNameOrder})")
                typer.echo(f"2) Sort by Price ({nextPriceOrder})")
                typer.echo(f"3) Define price range")
                typer.echo(f"4) Search by part name/keyword")
                typer.echo(f"5) Back to Component Selection")

                sortChoice = typer.prompt("Choose a sorting option", type=int)

                if sortChoice == 1:
                    sortCriteria, sortOrder = "name", (
                        "asc"
                        if sortCriteria != "name" or sortOrder == "desc"
                        else "desc"
                    )
                elif sortChoice == 2:
                    sortCriteria, sortOrder = "price", (
                        "asc"
                        if sortCriteria != "price" or sortOrder == "desc"
                        else "desc"
                    )
                elif sortChoice == 3:
                    min_price = typer.prompt("Enter minimum price (€)", type=float)
                    max_price = typer.prompt("Enter maximum price (€)", type=float)
                    active_price_range["min"], active_price_range["max"] = (
                        min_price,
                        max_price,
                    )
                elif sortChoice == 4:
                    search_input = typer.prompt(
                        "Enter search keyword (0 to clear)"
                    ).strip()
                    if search_input == "0":
                        search_term = None
                        typer.echo(
                            typer.style(
                                "Search keyword cleared.", fg=typer.colors.GREEN
                            )
                        )
                    else:
                        search_term = search_input.lower()
                        typer.echo(
                            typer.style(
                                f"Search keyword set to: {search_term}",
                                fg=typer.colors.GREEN,
                            )
                        )
                elif sortChoice == 5:
                    break

                # Reapply filters and sorting after changes
                sortedParts = applyFiltersAndSorting(parts)
                totalParts = len(sortedParts)
                totalPages = (totalParts + pageSize - 1) // pageSize
                currentPage = 0  # Reset to the first page
                typer.echo(
                    typer.style("Filters and sorting updated.", fg=typer.colors.GREEN)
                )

        # Handle page navigation
        elif choice == pageSize + 3 and currentPage < totalPages - 1:
            currentPage += 1
        elif choice == pageSize + 4 and currentPage > 0:
            currentPage -= 1
        elif choice == pageSize + 5:
            return  # Exit to Component Menu

        else:
            typer.echo(
                typer.style("Invalid choice. Please try again.", fg=typer.colors.RED)
            )


### Helper Function for Intelligent Suggestions
def suggestIntelligentComponents(componentType):
    """Display intelligent suggestions for the specified component type."""
    suggestionFunctions = {
        "gpu": suggestCompatibleGPUs,
        "psu": suggestCompatiblePSUs,
        "motherboard": suggestCompatibleMotherboards,
        "cpu": suggestCompatibleCPUs,
        "cpucooler": suggestCompatibleCPUcoolers,
        "ram": suggestCompatibleRAMs,
        "ssd": suggestCompatibleSSDs,
        "hdd": suggestCompatibleHDDs,
        "case": suggestCompatibleCases,
    }
    suggestFunc = suggestionFunctions.get(componentType)

    if suggestFunc:
        suggestions = suggestFunc(userPC, None)[:5]  # Get top 5 suggestions
        if suggestions:
            typer.echo(
                typer.style(
                    f"\nTop 5 {componentType.upper()} Suggestions:",
                    fg=typer.colors.YELLOW,
                )
            )
            for i, suggestion in enumerate(suggestions, start=1):
                typer.echo(f"{i}) {cleanName(suggestion.name)} - {suggestion.price}")
            typer.echo(
                typer.style(
                    "Use these suggestions to guide your choices.",
                    fg=typer.colors.GREEN,
                )
            )
        else:
            typer.echo(
                typer.style(
                    f"No intelligent suggestions available for {componentType.upper()}.",
                    fg=typer.colors.RED,
                )
            )
    else:
        typer.echo(
            typer.style(
                f"Unable to generate suggestions for {componentType.upper()}.",
                fg=typer.colors.RED,
            )
        )
        clearScreen()


def displayIncompatibilityMessages(comp, componentType, userPC):
    """Display any incompatibility messages."""
    # Filter out empty messages
    filteredMessages = {key: value for key, value in comp.messages.items() if value}

    if filteredMessages:
        typer.echo(
            typer.style(f"\nIssues with {componentType.upper()}:", fg=typer.colors.RED)
        )
        for key, msgs in filteredMessages.items():
            for message in msgs:
                typer.echo(f" - {message}")

        suggestAlternatives = typer.prompt(
            "Would you like to see a few compatible alternatives? (y/n)", type=str
        )
        if suggestAlternatives.lower() == "y":
            suggestComponent(userPC, componentType, comp)


def suggestComponent(userPC, componentType, comp):
    clearScreen()
    # Dictionary for all the suggestion functions
    suggestionFunctions = {
        "cpu": suggestCompatibleCPUs,
        "psu": suggestCompatiblePSUs,
        "gpu": suggestCompatibleGPUs,
        "case": suggestCompatibleCases,
        "cpucooler": suggestCompatibleCPUcoolers,
        "motherboard": suggestCompatibleMotherboards,
        "ram": suggestCompatibleRAMs,
        "ssd": suggestCompatibleSSDs,
        "hdd": suggestCompatibleHDDs,
    }
    suggestFunc = suggestionFunctions.get(componentType)

    if suggestFunc:
        while True:
            suggestedParts = suggestFunc(
                userPC, comp
            )  # Get 5 suggestions for the build
            been = 0
            if not suggestedParts:
                typer.echo(
                    typer.style(
                        f"\n<<< WARNING! No {componentType.upper()} suggestions could be made for your current build >>>",
                        fg=typer.colors.BRIGHT_RED,
                    )
                )
                differentMessage = {"hdd", "ssd", "ram"}
                if componentType not in differentMessage:
                    typer.echo(
                        typer.style(
                            f"<<< Please review the compatibility messages below again, as they may indicate the source of the issue and review your current build >>>",
                            fg=typer.colors.BRIGHT_GREEN,
                        )
                    )
                    for component, componentMessages in comp.messages.items():
                        if componentMessages:
                            typer.echo(
                                typer.style(
                                    f"\n--- {component.upper()} Compatibility Issues ---",
                                    fg=typer.colors.WHITE,
                                )
                            )
                    for message in componentMessages:
                        typer.echo(
                            typer.style(f" - {message}", fg=typer.colors.BRIGHT_WHITE)
                        )
                        return
                else:
                    been = 1
                    typer.echo(
                        typer.style(
                            f"<<< This might indicate that you have exceeded motherboard limits for the {componentType.upper()} part >>>",
                            fg=typer.colors.RED,
                        )
                    )
                    if userPC.selectedPart:
                        suggestAlternatives = typer.prompt(
                            "Would you like to see if we can find a suitable motherboard for your build? (y/n)",
                            type=str,
                        )
                        if suggestAlternatives.lower() == "y":
                            userPC.addComponent(componentType, userPC.selectedPart)
                            oldMotherboard = userPC.components["motherboard"][0]
                            userPC.removeComponent("motherboard", 0)
                            suggestComponent(userPC, "motherboard", comp)
                            userPC.removeComponent(
                                componentType, len(userPC.components[componentType]) - 1
                            )
                            if len(userPC.components["motherboard"]) == 1:
                                formatSpecifications(
                                    userPC.selectedPart.specs.to_dict()
                                )

                                confirmChoice = typer.prompt(
                                    "Do you want to add this to your build? (y/n)",
                                    type=str,
                                )

                                if confirmChoice.lower() == "y":
                                    userPC.addComponent(
                                        componentType, userPC.selectedPart
                                    )
                                    typer.echo(
                                        typer.style(
                                            f"{componentType.upper()} added to your build.",
                                            fg=typer.colors.GREEN,
                                        )
                                    )
                                    return
                                else:
                                    return
                            else:
                                userPC.addComponent("motherboard", oldMotherboard)
                        else:
                            return
            if suggestedParts:
                if (
                    componentType == "ssd"
                    and been != 1
                    and userPC.selectedPart
                    and hasattr(userPC.selectedPart, "specs")
                    and hasattr(userPC.selectedPart.specs, "interface")
                ):
                    ssdType = (
                        "M.2"
                        if any(
                            "M.2" in interface
                            for interface in userPC.selectedPart.specs.interface
                        )
                        else "SATA"
                    )
                    typer.echo(
                        typer.style(
                            f"\nSuggested compatible {ssdType} {componentType.upper()}s:",
                            fg=typer.colors.YELLOW,
                        )
                    )
                else:
                    typer.echo(
                        typer.style(
                            f"\nSuggested compatible {componentType.upper()}s:",
                            fg=typer.colors.YELLOW,
                        )
                    )

                for i, part in enumerate(suggestedParts, start=1):
                    typer.echo(f"{i}) {cleanName(part.name)} - {part.price}")

                # Giving user an option to choose
                skipOption = len(suggestedParts) + 1
                typer.echo(
                    typer.style(
                        f"{skipOption}) Skip adding a suggested part",
                        fg=typer.colors.YELLOW,
                    )
                )

                choice = typer.prompt(
                    f"Choose a suggested {componentType} to add or skip", type=int
                )

                if choice == skipOption:
                    typer.echo(
                        typer.style(
                            f"Skipping the addition of a suggested {componentType}.",
                            fg=typer.colors.GREEN,
                        )
                    )
                    break
                elif 1 <= choice <= len(suggestedParts):
                    selectedPart = suggestedParts[choice - 1]
                    typer.echo(
                        typer.style(
                            f"You selected {cleanName(selectedPart.name)} for {selectedPart.price}",
                            fg=typer.colors.YELLOW,
                        )
                    )
                    formatSpecifications(selectedPart.specs.to_dict())

                    confirmChoice = typer.prompt(
                        "Do you want to add this to your build? (y/n)", type=str
                    )

                    if confirmChoice.lower() == "y":
                        userPC.addComponent(componentType, selectedPart)
                        typer.echo(
                            typer.style(
                                f"{componentType.upper()} added to your build.",
                                fg=typer.colors.GREEN,
                            )
                        )
                        break
                    else:
                        typer.echo(
                            typer.style(
                                "\nSelection cancelled. You can choose another part or skip.",
                                fg=typer.colors.RED,
                            )
                        )
                else:
                    typer.echo(
                        typer.style(
                            "Invalid choice. Please try again.", fg=typer.colors.RED
                        )
                    )
                    clearScreen()
            else:
                return
    else:
        typer.echo(
            typer.style(
                f"\nNo compatible alternatives found for {componentType}.",
                fg=typer.colors.RED,
            )
        )


def viewPurchase():
    clearScreen()
    """View the current purchase and total price."""
    typer.echo(typer.style("\n--- Current Build ---", fg=typer.colors.YELLOW))
    userPC.display()


def getComponents(componentType):
    """Fetch components based on the type (GPU or PSU)"""
    try:
        if componentType == "gpu":
            return loadGPUsfromJSON()
        elif componentType == "psu":
            return loadPSUsfromJSON()
        elif componentType == "motherboard":
            return loadMBsfromJSON()
        elif componentType == "cpu":
            return loadCPUsfromJSON()
        elif componentType == "cpucooler":
            return loadCPUCoolersfromJSON()
        elif componentType == "ram":
            return loadRAMsfromJSON()
        elif componentType == "ssd":
            return loadSSDsfromJSON()
        elif componentType == "hdd":
            return loadHDDsfromJSON()
        elif componentType == "case":
            return loadCasesfromJSON()
    except Exception as e:
        typer.echo(
            typer.style(
                f"An error occurred while fetching {componentType.upper()} data. Please try again later.",
                fg=typer.colors.RED,
            )
        )
    return []


def finishBuild():
    clearScreen()
    """Finalize and display the build"""
    typer.echo(typer.style("\n--- Final Build ---", fg=typer.colors.YELLOW))
    userPC.display()

    while True:
        typer.echo(typer.style("1) Confirm build", fg=typer.colors.GREEN))
        typer.echo(typer.style("2) Return to Main Menu", fg=typer.colors.MAGENTA))
        action = typer.prompt("Choose an option", type=int)

        if action == 1:
            typer.echo(
                typer.style(
                    "Build confirmed. Thank you for using the PC Builder App!",
                    fg=typer.colors.GREEN,
                )
            )
            sys.exit()  # Exit the program
        elif action == 2:
            clearScreen()
            return  # Return to go back to main menu
        else:
            typer.echo(
                typer.style("Invalid choice, please try again.", fg=typer.colors.RED)
            )
            clearScreen()


def removeComponent():
    clearScreen()
    """Remove a component from the build if it exists."""

    # List component types that are available to remove
    componentOptions = [
        ("gpu", "Remove GPU"),
        ("psu", "Remove PSU"),
        ("motherboard", "Remove motherboard"),
        ("cpu", "Remove CPU"),
        ("cpucooler", "Remove CPU cooler"),
        ("ram", "Remove RAM"),
        ("ssd", "Remove SSD"),
        ("hdd", "Remove HDD"),
        ("case", "Remove case"),
    ]

    while True:
        typer.echo(
            typer.style(
                "\n--- Select a Component to Remove ---", fg=typer.colors.YELLOW
            )
        )
        optionNum = 1
        validOptions = {}
        componentsExist = False

        # Display only the components that are in the user's build
        for compType, label in componentOptions:
            if userPC.components[compType]:
                componentsExist = True
                typer.echo(f"{optionNum}) {label}")
                validOptions[optionNum] = compType
                optionNum += 1

        # Dynamically add option to remove all components if any exist
        if componentsExist:
            typer.echo(
                typer.style(
                    f"{optionNum}) Remove all components", fg=typer.colors.BRIGHT_RED
                )
            )
            removeAllOption = optionNum
            optionNum += 1

        typer.echo(
            typer.style(f"{optionNum}) Back to previous menu", fg=typer.colors.CYAN)
        )

        choice = typer.prompt("Choose a component to remove", type=int)

        if choice in validOptions:
            compType = validOptions[choice]

            # Handle components that allow multiple instances
            if compType in ["ram", "ssd", "hdd"]:
                typer.echo(f"\n--- Available {compType.upper()}s ---")
                for i, part in enumerate(userPC.components[compType], start=1):
                    typer.echo(f"{i}) {cleanName(part.name)} - {part.price}")

                partChoice = typer.prompt(
                    f"Select {compType.upper()} to remove or choose '0' to remove all",
                    type=int,
                )

                # Check if user wants to remove all
                if partChoice == 0:
                    confirm = typer.prompt(
                        f"Are you sure you want to remove all {compType.upper()}s? (y/n)",
                        type=str,
                    )
                    if confirm.lower() == "y":
                        for part in userPC.components[compType]:
                            price = float(
                                part.price.replace("€", "").replace("$", "").strip()
                            )
                            userPC.totalPrice -= price
                        userPC.components[compType] = []
                        typer.echo(
                            typer.style(
                                f"All {compType.upper()}s removed from your build.",
                                fg=typer.colors.GREEN,
                            )
                        )
                    else:
                        typer.echo(
                            typer.style("Operation cancelled.", fg=typer.colors.RED)
                        )
                elif 1 <= partChoice <= len(userPC.components[compType]):
                    partToRemove = userPC.components[compType][partChoice - 1]
                    confirm = typer.prompt(
                        f"Are you sure you want to remove {cleanName(partToRemove.name)}? (y/n)",
                        type=str,
                    )
                    if confirm.lower() == "y":
                        userPC.removeComponent(compType, partChoice - 1)
                        typer.echo(
                            typer.style(
                                f"{compType.upper()} removed from your build.",
                                fg=typer.colors.GREEN,
                            )
                        )
                    else:
                        typer.echo(
                            typer.style("Operation cancelled.", fg=typer.colors.GREEN)
                        )
                else:
                    typer.echo(
                        typer.style(
                            "Invalid choice, please try again.", fg=typer.colors.RED
                        )
                    )
                    clearScreen()

            else:
                partToRemove = userPC.components[compType][0]
                confirm = typer.prompt(
                    f"Are you sure you want to remove {cleanName(partToRemove.name)}? (y/n)",
                    type=str,
                )
                if confirm.lower() == "y":
                    userPC.removeComponent(compType, 0)
                    typer.echo(
                        typer.style(
                            f"{compType.upper()} removed from your build.",
                            fg=typer.colors.GREEN,
                        )
                    )
                else:
                    typer.echo(
                        typer.style("Operation cancelled.", fg=typer.colors.GREEN)
                    )

            # Display updated build
            typer.echo(typer.style("\n--- Updated Build ---", fg=typer.colors.YELLOW))
            userPC.display()

        # Handle 'Remove all components' choice dynamically
        elif componentsExist and choice == removeAllOption:
            confirm = typer.prompt(
                "Are you sure you want to remove all components? (y/n)", type=str
            )
            if confirm.lower() == "y":
                for key in userPC.components:
                    userPC.components[key] = []
                userPC.totalPrice = 0.00
                typer.echo(
                    typer.style(
                        "All components have been removed from your build.",
                        fg=typer.colors.GREEN,
                    )
                )
                userPC.display()
            else:
                typer.echo(typer.style("Operation cancelled.", fg=typer.colors.GREEN))

        elif choice == optionNum:
            clearScreen()
            return

        else:
            typer.echo(
                typer.style("Invalid choice, please try again.", fg=typer.colors.RED)
            )
            clearScreen()


if __name__ == "__main__":
    app()
