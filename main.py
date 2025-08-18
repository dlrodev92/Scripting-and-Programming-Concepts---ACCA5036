"""
Bakery Inventory System 
-----------------------
# Author: David Lopez Rodriguez
# Student No: 2336542
# Module: ACCA5036 - Scripting and Programming Concepts
# Date: August 2025
# Description: This program manages a bakery inventory, allowing users to add, update, search, and delete ingredients.
# To run this program, simply execute the script in a Python environment by using the command: python main.py.
"""

inventory = {}

'''# Helper functions to be used across the program and to help not repeat code'''
def normalize_name(name):
    ''' this function cleans up the input spaces and converts it to lower case'''

    normalized = name.strip().lower()
    if not normalized:
        return None
    else:
        return normalized

def verify_input(name):
    '''this function checks if the name or the unit is valid, only allows for alphabetical characters'''
    return name and name.isalpha()

def check_ingredient_exists(inventory, name):
    return name in inventory  

def verify_number(prompt, allow_negative=False):
    while True:
        try:
            value = float(input(prompt))
            if not allow_negative and value < 0:
                print("Quantity cannot be negative. Please try again.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def exit_from_mode(input_prompt):
    '''this function is used to let the user exit from a mode or continue, it checks the input string and returns True or False'''
    while True:
        exit_input = input(input_prompt).strip().lower()
        if exit_input == 'exit':
            return True
        elif exit_input == 'c':
            return False
        else:
            print("Invalid type. Please type 'exit' to exit or press 'c' to continue.")

def display_error_message(message):
    '''to display error message in a consistent and clear format '''
    print("\n" + "=" * 40)
    print(message)
    print("-" * 40 + "\n")
    
def display_inventory(items):
    '''this function displays the inventory in a formated way, either for one or multiple items'''
    
    print("\nCurrent Inventory:")
    print(f"{'Name':<20} {'Quantity':<10} {'Unit':<10}")
    print("-" * 40)
    for item in sorted(items.values(), key=lambda x: x['display_name'].lower()):
        print(item['display_name'].ljust(20),
              str(f"{item['cuantity']:.2f}").ljust(10),
              item['unit'].ljust(10))
    print("-" * 40)

def validate_name(input_name):
    ''' this functions validates that the name is normalized and not empty'''
    normalized = normalize_name(input_name)
    if not normalized:
        display_error_message("Ingredient name cannot be empty. Please try again")
        return None
    if not verify_input(normalized):
        display_error_message("Invalid ingredient name. Please use alphabetic characters only.")
        return None
    return normalized


'''# core program functions '''

def list_ingredients(inventory):
   while True:
        if not inventory:
            display_error_message("No ingredients in inventory.")
        else:
            display_inventory(inventory)
        if exit_from_mode("\nType 'exit' to return to the main menu:"):
            break

def update_quantity(inventory, name=None):
    while True:
        
        if name is None:
            name = input("Enter ingredient name to update: ")
            normalized_name = validate_name(name)
        else:
            normalized_name = validate_name(name)
            
        if not normalized_name:
            return None

        if not check_ingredient_exists(inventory, normalized_name):
            display_error_message(f"{name} does not exist in inventory.")
            return None

       
        delta = verify_number("Enter quantity change (can be negative): ", allow_negative=True)
        new_cuantity = inventory[normalized_name]['cuantity'] + delta

        if new_cuantity < 0:
            display_error_message("Resulting quantity cannot be negative. Update cancelled.")
            return None

        inventory[normalized_name]['cuantity'] = new_cuantity
        print(f"Updated {name}. New quantity: {new_cuantity} {inventory[normalized_name]['unit']}")

        
        if exit_from_mode("\nType 'c' to continue or type 'exit' to return to the main menu: "):
            break

        return delta  

def add_ingredient(inventory):
    while True:
        name = input("Enter ingredient name: ")
        normalized_name = validate_name(name)
        if not normalized_name:
            continue
        
        if check_ingredient_exists(inventory, normalized_name):
            action = input(f"{name} already exists. Do you want to (I)ncrease, (R)eplace, or (C)ancel? ").strip().upper()
            if action == 'I':
                delta = update_quantity(inventory, normalized_name)
                if delta is not None:
                    inventory[normalized_name]['cuantity'] += delta
                    print(f"Increased {name} by {delta}. New quantity: {inventory[normalized_name]['cuantity']} {inventory[normalized_name]['unit']}")
            elif action == 'R':
                cuantity = verify_number("Enter new quantity: ")
                unit = input("Enter unit: ").strip()
                if not verify_input(unit):
                    display_error_message("Invalid unit. Please use alphabetic characters only.")
                    return
                inventory[normalized_name] = {"display_name": name, "cuantity": cuantity, "unit": unit}
                print(f"Replaced {name} with new quantity: {cuantity} {unit}")
            elif action == 'C':
                display_error_message("Action cancelled.")
            else:
                display_error_message("Invalid choice. Action cancelled.")
        else:
            cuantity = verify_number("Enter quantity: ")
            unit = input("Enter unit: ").strip()
            if not verify_input(unit):
                display_error_message("Invalid unit. Please use alphabetic characters only.")
                return
            inventory[normalized_name] = {"display_name": name, "cuantity": cuantity, "unit": unit}
            print(f"Added {name} with quantity: {cuantity} {unit}")

        if exit_from_mode("\nPress 'c' to add a new ingredient or type 'exit' to return to the main menu: "):
            break

def search_ingredients(inventory):
    while True:
        searched_name = validate_name(input("Enter ingredient name to search: "))
        
        if not searched_name:
            return
        
        matches = {k: v for k, v in inventory.items() if searched_name in k.lower()}

        if not matches:
            display_error_message(f"No ingredients found matching '{searched_name}'.")
            return

        display_inventory(matches)
        
        if exit_from_mode("\nPress 'c' to search again or type 'exit' to return to the main menu: "):
            break

def delete_ingredient(inventory,name=None):
    while True:
        if name is None:
            name = input("Enter ingredient name to delete: ")
            normalized_name = validate_name(name)
        else:
            normalized_name = validate_name(name)

        if not normalized_name:
            return
        
        if not verify_input(normalized_name):
            display_error_message("Invalid ingredient name. Please use alphabetic characters only.")
            return
        
        if not check_ingredient_exists(inventory, normalized_name):
            display_error_message(f"{name} does not exist in inventory.")
            return
        
        del inventory[normalized_name]
        print(f"Deleted {name} from inventory.")
        
        if exit_from_mode("\nPress 'c' to delete another ingredient or type 'exit' to return to the main menu: "):
            break


'''# Menu System Main Function '''

def show_menu():
    
    print("\nBakery Inventory Menu:")
    print("1. Add ingredient")
    print("2. List ingredients")
    print("3. Update quantity")
    print("4. Search ingredient")
    print("5. Delete ingredient")
    print("0. Exit")
    
    choice = input("Enter your choice: ").strip()
    if choice in ['0', '1', '2', '3', '4', '5']:
        return choice


def main():
    while True:
        choice = show_menu()
        
        if choice == '0':
            print("Closing The Bakery Inventory System. Goodbye!")
            break
        elif choice == '1':
            add_ingredient(inventory)
        elif choice == '2':
            list_ingredients(inventory)
        elif choice == '3':
            update_quantity(inventory)
        elif choice == '4':
            search_ingredients(inventory)
        elif choice == '5':
            delete_ingredient(inventory)
        else:
            display_error_message("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        display_error_message("Program interrupted. Exiting...")
