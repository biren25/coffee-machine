class Ingredient(object):
    """
    Ingredients for Coffee Machine.
    For simplicity, all the quantities are in one universal unit. 
    As in not 'ml' for milk or not 'gm' for coffee powder.
    """

    def __init__(self, ingredientName, availableQuantity, minimumQuntity=50):
        """
        if availableQuantity < minimumQuntity -> refill required.
        minimumQuntity is 50 by default. Could enhance as per requirement.
        """
        self.ingredientName = ingredientName
        self.minimumQuntity = minimumQuntity
        self.availableQuantity = availableQuantity

    def isAvailable(self, requiredQuantity):
        return self.availableQuantity >= requiredQuantity
    
    def use(self, quantity):
        """
        provides required quantity of the ingredient if available.
        """
        if self.isAvailable(quantity):
            self.availableQuantity -= quantity
            return True
        print(self.ingredientName + " not available")
        return False

    def refill(self, quantity):
        """
        Updates quantity for usage
        """
        self.availableQuantity += quantity
        return
