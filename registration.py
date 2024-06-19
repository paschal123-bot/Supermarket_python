class User:
    def __init__(self, firstName, lastName, email, password): 
        self.firstName = firstName
        self.lastName = lastName
        self.password = password
        self.email = email

    def to_dict(self):
        return {
            'First Name': self.firstName,
            'Last Name': self.lastName,
            'Email': self.email,
            'Password': self.password
        }

# Store user and item object arrays
user_list = []
item_list = []

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

def initialize_supermarket():
    predefined_items = [
        Items("Yam", "food", 1000000, 5000000),
        Items("Beans", "food", 20000000, 1000000),
        Items("Rice", "food", 30000000, 2000000),
        Items("Golden Morn", "food", 15000000, 800000),
        Items("Cornflakes", "food", 18000000, 1200000),
        Items("Shirt", "clothes", 50000000, 6000000),
        Items("Jeans", "clothes", 7000000, 400000),
        Items("Singlet", "clothes", 1000000, 7000000),
        Items("Boxers", "clothes", 1500000, 5000000),
        Items("Notebook", "books", 20000000, 15000000),
        Items("Pen", "books", 5000000, 50000000),
        Items("Pencil", "books", 3000000, 400000),
        Items("Eraser", "books", 2000000, 3000000),
        Items("Sharpener", "books", 2500000, 2500000),
        Items("Toothpaste", "provisions", 3500000, 1000000),
        Items("Soap", "provisions", 2500000, 2000000),
        Items("Dettol", "detergents", 400000, 180000),
        Items("Omo", "detergents", 500000, 220000)
    ]
    item_list.extend(predefined_items)
    print("Supermarket initialized with predefined items.")

def get_user_input():
    first_name = input("Enter your First Name: ")
    last_name = input("Enter your Last Name: ")
    email = input("Enter your Email: ")
    return first_name, last_name, email

def register_user():
    first_name, last_name, email = get_user_input()
    while True:
        password = input("Enter your Password: ")
        confirm_password = input("Enter your Confirm Password: ")

        if password != confirm_password:
            print("Passwords do not match. Please try again.")
        else:
            user = User(first_name, last_name, email, password)
            user_list.append(user)
            print("Registration successful.")
            break

def login_user():
    email = input("Enter your Email: ")
    password = input("Enter your Password: ")
    for user in user_list:
        if user.email == email and user.password == password:
            print("Login successful.")
            return True
    print("Invalid email or password.")
    return False

def display_items():
    print("Items in the Supermarket:")
    for item in item_list:
        print(item.to_dict())

def search_item(name):
    for item in item_list:
        if item.name.lower() == name.lower():
            return item
    return None

def order_items():
    cart = []
    total_cost = 0

    while True:
        display_items()
        item_name = input("Enter the name of the item you want to order: ")
        item = search_item(item_name)
        if item:
            quantity = int(input(f"Enter quantity of {item.name}: "))
            if quantity <= item.quantity:
                cart.append((item, quantity))
                total_cost += item.price * quantity
                item.quantity -= quantity
            else:
                print("Insufficient stock.")
        else:
            print("Item not found.")
        
        more = input("Do you want to order another item? (yes/no): ").lower()
        if more == 'no':
            break
    
    print("Proceed to payment.")
    account_number = input("Enter the supermarket account number for payment: ")
    print(f"Payment of {total_cost} successful to account number {account_number}.")
    
    print("\nReceipt")
    print("-------")
    for item, quantity in cart:
        print(f"{item.name}: {quantity} x {item.price} = {quantity * item.price}")
    print(f"Total Cost: {total_cost}")
    print("Thanks for visiting Paschal's Supermarket")

def main():
    initialize_supermarket()
    print("Hello Everyone!!")
    while True:
        print("\n--- Paschal's Supermarket ---")
        print("1. Register User")
        print("2. Login User")
        print("3. Display Items")
        print("4. Order Items")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            register_user()
        elif choice == '2':
            if login_user():
                while True:
                    print("\n--- User Menu ---")
                    print("1. Order Items")
                    print("2. Logout")
                    user_choice = input("Enter your choice: ")
                    if user_choice == '1':
                        order_items()
                    elif user_choice == '2':
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif choice == '3':
            display_items()
        elif choice == '4':
            order_items()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
