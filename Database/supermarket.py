class Items:
    def __init__(self, name, category, price, quantity):
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity

    def to_dict(self):
        return {
            'Name': self.name,
            'Category': self.category,
            'Price': self.price,
            'Quantity': self.quantity
        }

# Store object array
item_list = []

def initialize_supermarket():
    predefined_items = [
         Items("Yam", "food", 10000000, 50000000),
        Items("Beans", "food", 20000000, 1000000),
        Items("Rice", "food", 30000000, 2000000),
        Items("Golden Morn", "food", 15000000, 800000),
        Items("Cornflakes", "food", 180000000, 1200000),
        Items("Shirt", "clothes", 50000000, 6000000),
        Items("Jeans", "clothes", 70000000, 4000000),
        Items("Singlet", "clothes", 1000000, 70000000),
        Items("Boxers", "clothes", 15000000, 50000000),
        Items("Notebook", "books", 20000000, 150000000),
        Items("Pen", "books", 500000, 5000000),
        Items("Pencil", "books", 300000, 4000000),
        Items("Eraser", "books", 2000000, 30000000),
        Items("Sharpener", "books", 2500000, 25000000),
        Items("Toothpaste", "provisions", 3500000, 1000000),
        Items("Soap", "provisions", 2500000, 2000000),
        Items("Dettol", "detergents", 4000000, 1800000),
        Items("Omo", "detergents", 5000000, 2200000)
        
    ]
    item_list.extend(predefined_items)
    print("Supermarket initialized with predefined items.")

def get_item_input():
    name = input("Enter item name: ")
    category = input("Enter item category (food, provisions, clothes, books): ")
    price = float(input("Enter item price: "))
    quantity = int(input("Enter item quantity: "))
    return name, category, price, quantity

def display_items():
    print("Items in the Supermarket:")
    for item in item_list:
        print(item.to_dict())

def add_item():
    name, category, price, quantity = get_item_input()
    item = Items(name, category, price, quantity)
    item_list.append(item)
    print("Item added successfully.")

def search_item(name):
    for item in item_list:
        if item.name.lower() == name.lower():
            return item
    return None

def remove_item(name):
    item = search_item(name)
    if item:
        item_list.remove(item)
        print("Item removed successfully.")
    else:
        print("Item not found.")

def main():
    initialize_supermarket()
    while True:
        print("\n--- Supermarket Management ---")
        print("1. Add Item")
        print("2. Display Items")
        print("3. Search Item")
        print("4. Remove Item")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_item()
        elif choice == '2':
            display_items()
        elif choice == '3':
            name = input("Enter item name to search: ")
            item = search_item(name)
            if item:
                print("Item found:", item.to_dict())
            else:
                print("Item not found.")
        elif choice == '4':
            name = input("Enter item name to remove: ")
            remove_item(name)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
