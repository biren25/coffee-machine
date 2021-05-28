import time

from multiprocessing import Process, Queue

from machine import CoffeeMachine, serve_beverages
from ingredients import Ingredient
from beverages import Beverage
from constants import NO_OF_OUTLETS, INITAL_INGREDIENTS, BEVRAGES_RECIPE


if __name__ == '__main__':
    
    ingredients_map = {}
    beverages_map = {}

    # Creating ingredients objects. Will be connected with Machine
    for an_ingredient, quantity in INITAL_INGREDIENTS.items():
        ingredient_obj = Ingredient(an_ingredient, quantity)
        ingredients_map[an_ingredient] = ingredient_obj

    # Creating beverages objects. Will be connected with Machine
    for a_beverage in BEVRAGES_RECIPE:
        recipe = {}
        for an_ingredient in BEVRAGES_RECIPE[a_beverage]:
            if an_ingredient in ingredients_map:
                ingredient_obj = ingredients_map[an_ingredient]
            else:
                ingredient_obj = Ingredient(an_ingredient, 0)
                ingredients_map[an_ingredient] = ingredient_obj
            recipe[ingredient_obj] = BEVRAGES_RECIPE[a_beverage][an_ingredient]
        bevergae_obj = Beverage(a_beverage, recipe)
        beverages_map[a_beverage] = bevergae_obj


    coffee_machine = CoffeeMachine(NO_OF_OUTLETS)
    coffee_machine.ingredients = ingredients_map
    coffee_machine.beverages = beverages_map
    
    # Queue will be used for parallel processing. 
    # One outlet - one process
    q = Queue()        


    # Below code is for I/O ops

    automated_instructions = [
        "hot_coffee hot_tea green_tea",
        "CHECK",
        "REFILL",
        "green_mixture 100",
        "CHECK",
        "black_tea",
        "REFILL",
        "hot_water 500",        
        "hot_coffee hot_tea"
    ]

    auto_mode = False
    first_time = True
    
    while True:
    
        q.put(coffee_machine)    
        
        if first_time:
            print("Welcome to the Coffee House!")
            coffee_machine.printMenu()
            print("Enter beverage names to order. You can get upto 3 drinks at once since the machine has 3 outlets.")
            print("Ex. 'black_tea hot_coffee hot_tea' or 'black_tea hot_coffee'")
            print("Enter 'CHECK' to see quatity of all the ingredients and if any of them needs refill")
            print("Enter 'REFILL' to refill any of the ingreditents")
            print("Enter 'MENU' to see the menu again")
            print("Enter 'AUTO' for automated instructions.")
            print("Press ctrl+C or enter 'EXIT' to exit")
            first_time = False

        if auto_mode:
            time.sleep(1)
            if automated_instructions:
                user_input = automated_instructions.pop(0)
            else:
                break
            
            print(user_input)
            time.sleep(1)
        else:
            user_input = input()

        if user_input == "MENU":
            coffee_machine = q.get()
            coffee_machine.printMenu()
            q.put(coffee_machine)
     
        elif user_input == "CHECK":
            coffee_machine = q.get()
            coffee_machine.printAvailableIngredients()
            q.put(coffee_machine)
     
        elif user_input == "REFILL":
            print("Enter ingredient name along with quantity to refill. Ex. 'hot_water 100'")
            if auto_mode:
                time.sleep(1)
                if automated_instructions:
                    user_input = automated_instructions.pop(0)
                    print(user_input)
                    time.sleep(1)
                else:
                    break
            else:
                user_input = input()
           
            try:
                ingredient_name, quantity = user_input.split()
            except:
                print("Invalid input")
            if ingredient_name not in ingredients_map:
                print("Invalid input")
                continue
            coffee_machine = q.get()
            coffee_machine.refillIngredient(ingredient_name, int(quantity))
            q.put(coffee_machine)
      
        elif user_input == "EXIT":
            break
      
        elif user_input == "AUTO":
            auto_mode = True            
      
        else:
            orders = user_input.split()
            if not orders or len(orders)>NO_OF_OUTLETS:
                print("Invalid input")
                continue
            
            invalid_order = False
            for an_order in orders:
                if an_order not in BEVRAGES_RECIPE:
                    print("Invalid input -- "+an_order)
                    invalid_order = True
                    break
            
            if invalid_order:
                continue
           
            processes = []
            for order in orders:
                processes.append(Process(target=serve_beverages, args=(q, order)))  

            for process in processes:
                process.start()

            for process in processes:
                process.join()

            coffee_machine = q.get()    