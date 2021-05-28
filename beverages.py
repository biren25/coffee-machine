import time

class Beverage(object):
    """
    Beverages for Coffee Machine.
    """

    def __init__(self, beverageName, recipe={}):
        """
        `recipe` is dictionary type object. key - ingredient object, value - required quantity.
        """
        self.beverageName = beverageName
        self.recipe = recipe

    def prepareBeverage(self, queue, machine):
        """
        Combines all the ingredients and prepares the beverage if available.
        This would take about 2 seconds(sleep added for simulation purpose).
        Only pouring part happens in parallel.
        """
        is_available, unavailable_ingredient  = self.getAllIngredients()

        # unblocks the acquiring process for other outlets /
        # once all ingredients are acquired.
        queue.put(machine)      
        
        if is_available:
            self.pour()
            return True
        else:
            print(self.beverageName + " cannot be prepared as "+ unavailable_ingredient +" is not available.")
            return False

    def isAvailable(self):
        """
        Checks if beverage is available by checking availibility of all the required ingredients
        """
        for an_ingredient in self.recipe:
            if not an_ingredient.isAvailable(self.recipe[an_ingredient]):
                return False, an_ingredient.ingredientName
        return True, ""

    def getAllIngredients(self):
        """
        Combines all the ingredients required for the drink.
        This part is not done in parallel to avoid race condition.
        """
        is_available, unavailable_ingredient = self.isAvailable()
        if is_available:
            for an_ingredient in self.recipe:
                an_ingredient.use(self.recipe[an_ingredient])
            return True, ""
        else:
            return False, unavailable_ingredient

    def pour(self):
        """
        Simulates the pouring behaviour.
        """
        print(self.beverageName+ " pouring started.")
        time.sleep(2)
        print(self.beverageName + " is prepared.")
