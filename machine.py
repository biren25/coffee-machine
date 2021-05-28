
class CoffeeMachine(object):
    """
    handles all the actions like showing menu, getting beverage, refilling.
    """

    def __init__(self, outlets=1, ingredients={}, beverages={}):
        """
        `ingredients` is dictionary type object. key - ingredient name, value - ingredient object.
        `beverages` is dictionary type object. key - beverage name, value - beverage object.
        """
        self.outlets = outlets
        self.ingredients = ingredients
        self.beverages = beverages

    def printMenu(self):
        """
        Prints all the beverages machine can prepare.
        """
        print("Here is the menu. ")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        for a_beverage_name in self.beverages:
            print(a_beverage_name)
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        print()

    def printAvailableIngredients(self):
        """
        Prints available quantity for all the ingredients. 
        Also, shows alerts for refill if available quantity is less then minimum
        quantity. (min quantity is fixed at 50 as of now.)
        """
        for an_ingredient in self.ingredients:
            ingredient_obj = self.ingredients[an_ingredient]
            quantity_statement = an_ingredient+" : "+str(ingredient_obj.availableQuantity)
            if self.ingredients[an_ingredient].availableQuantity < self.ingredients[an_ingredient].minimumQuntity:
                quantity_statement += " -- needs refill"
            print(quantity_statement)
        return
            
    def refillIngredient(self, ingredientName, quantity):
        """
        Refills the ingredient.
        """
        ingredient_obj = self.ingredients[ingredientName]
        ingredient_obj.refill(quantity)
        print("Refill done.")
        return

    def getBeverage(self, beverageName, queue):
        """
        Prepares bevarage.
        Checks if all the ingredients reqired are available. 
        Uses the ingredients only if all are available. 
        Hence, this part(checking and fetching ingredients) is not done in parallel
        to avoid race condition.
        """
        if beverageName in self.beverages:
            bevarage_obj = self.beverages[beverageName]
            is_served = bevarage_obj.prepareBeverage(queue, self)
            if not is_served:
                return False    
            return True            
        else:
            return False

    def isBeverageAvailable(self, beverageName):
        """
        Checks availibilty of beverage. Not in use at the moment.
        Could be used to fetch only available beverages.
        """
        if beverageName in self.beverages:
            bevarage_obj = self.beverages[beverageName]
            return bevarage_obj.isAvailable()
        else:
            print("Beverage not found!")
            return False

    

def serve_beverages(queue, beverageName):
    """
    Helper function to serve the beverages.
    At most 3 processes can run in parallel. (3 - no of outlets).
    So to avoid ingredients being blocked by diff processes(outlets) at once 
    (race condition), we allow another process to start only after the 
    ingredients are allocated to the current process.
    
    Example, say there is 100 ml of hot_water available. 
    2 users are requesting hot_coffee at same time, we cannot serve to both of them.
    So we allocate 100 ml water (and other required ingredients) to one outlet
    and then only another outlet can check for availibility.
    """
    coffee_machine = queue.get()
    coffee_machine.getBeverage(beverageName, queue)  