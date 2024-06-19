from tabulate import tabulate
import re
import csv

class User:
    ROLES = ['CEO', 'admin', 'buyer']

    def __init__(self, firstName, lastName, email, password, role="buyer"): 
        self.firstName = firstName
        self.lastName = lastName
        self.password = password
        self.email = email
        self.role = role

    def to_dict(self):
        return {
            'First Name': self.firstName,
            'Last Name': self.lastName,
            'Email': self.email,
            'Password': self.password,
            'Role': self.role
        }

    @staticmethod
    def from_dict(data):
        return User(
            firstName=data['First Name'],
            lastName=data['Last Name'],
            email=data['Email'],
            password=data['Password'],
            role=data['Role']
        )

# Store user and item object dictionaries
user_dict = {}
item_dict = {}
session = None  # To keep track of the current user session

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

    @staticmethod
    def from_dict(data):
        return Items(
            name=data['Name'],
            category=data['Category'],
            price=data['Price'],
            quantity=data['Quantity']
        )

def initialize_supermarket():
    predefined_items = [
        Items("Yam", "food", 1000, 50),
        Items("Beans", "food", 2000, 100),
        Items("Rice", "food", 3000, 200),
        Items("Golden Morn", "food", 1500, 80),
        Items("Cornflakes", "food", 1800, 120),
        Items("Shirt", "clothes", 5000, 60),
        Items("Jeans", "clothes", 7000, 40),
        Items("Singlet", "clothes", 1000, 70),
        Items("Boxers", "clothes", 1500, 50),
        Items("Notebook", "books", 2000, 150),
        Items("Pen", "books", 500, 500),
        Items("Pencil", "books", 300, 40),
        Items("Eraser", "books", 200, 30),
        Items("Sharpener", "books", 250, 25),
        Items("Toothpaste", "provisions", 350, 100),
        Items("Soap", "provisions", 250, 200),
        Items("Dettol", "detergents", 400, 18),
        Items("Omo", "detergents", 500, 22)
    ]
    for item in predefined_items:
        item_dict[item.name] = item
    print("Supermarket initialized with predefined items.")

def get_user_input():
    first_name = input("Enter your First Name: ")
    last_name = input("Enter your Last Name: ")

    while True:
        email = input("Enter your Email: ")
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            break
        else:
            print("Invalid email format. Please try again.")

    return first_name, last_name, email

def save_user_to_file(user):
    with open('users.csv', mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['First Name', 'Last Name', 'Email', 'Password', 'Role'])
        writer.writerow(user.to_dict())

def save_user_to_file_as_dict(user):
    with open('users.csv', mode='a', newline='') as file:
        fieldnames = ['First Name', 'Last Name', 'Email', 'Password', 'Role']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Check if file is empty to write headers
        file.seek(0, 2)  # Move to the end of file
        file_empty = file.tell() == 0
        if file_empty:
            writer.writeheader()

        writer.writerow(user.to_dict())

def register_user():
    first_name, last_name, email = get_user_input()
    while True:
        password = input("Enter your Password: ")
        confirm_password = input("Enter your Confirm Password: ")

        if password != confirm_password:
            print("Passwords do not match. Please try again.")
        else:
            role = input("Enter role (CEO/admin/buyer): ")
            if role not in User.ROLES:
                print("Invalid role. Please choose from CEO, admin, or buyer.")
                continue
            user = User(first_name, last_name, email, password, role)
            user_dict[email] = user
            save_user_to_file_as_dict(user)
            print("Registration successful.")
            break

def load_users_from_file():
    try:
        with open('users.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user = User.from_dict(row)
                user_dict[user.email] = user
    except FileNotFoundError:
        pass

def login_user():
    global session
    email = input("Enter your Email: ")
    password = input("Enter your Password: ")
    user = user_dict.get(email)
    if user and user.password == password:
        print("Login successful.")
        session = user  # Set the current session to the logged-in user
        return user
    print("Invalid email or password.")
    return None

def logout_user():
    global session
    session = None  # Clear the session
    print("Logout successful.")

def display_items():
    if session and session.role in ['CEO', 'admin']:
        table = []
        for item in item_dict.values():
            table.append([item.name, item.category, item.price, item.quantity])
        headers = ["Name", "Category", "Price", "Quantity"]
        print(tabulate(table, headers, tablefmt="grid"))
    else:
        print("You do not have permission to view items.")

def search_item(name):
    if session and session.role in ['CEO', 'admin']:
        return item_dict.get(name)
    else:
        print("You do not have permission to search for items.")
        return None

def add_item():
    if session and session.role in ['CEO', 'admin']:
        name = input("Enter the name of the item: ")
        category = input("Enter the category of the item: ")
        price = int(input("Enter the price of the item: "))
        quantity = int(input("Enter the quantity of the item: "))
        new_item = Items(name, category, price, quantity)
        item_dict[name] = new_item
        print(f"Item {name} added successfully.")
    else:
        print("You do not have permission to add items.")

def order_items():
    if session:
        cart = []
        total_cost = 0

        while True:
            item_name = input("Enter the name of the item you want to order: ")
            item = item_dict.get(item_name)
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
    else:
        print("You need to login to order items.")

def main():
    load_users_from_file()
    initialize_supermarket()
    print("Hello Everyone!!")
    while True:
        print("\n--- Paschal's Supermarket ---")
        print("1. Register User")
        print("2. Login User")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            register_user()
        elif choice == '2':
            user = login_user()
            if user:
                while True:
                    if user.role in ['CEO', 'admin']:
                        print("\n--- Admin Menu ---")
                        print("1. Display Items")
                        print("2. Add Item")
                        print("3. Logout")
                        admin_choice = input("Enter your choice: ")
                        if admin_choice == '1':
                            display_items()
                        elif admin_choice == '2':
                            add_item()
                        elif admin_choice == '3':
                            logout_user()
                            break
                        else:
                            print("Invalid choice. Please try again.")
                    else:
                        print("\n--- User Menu ---")
                        print("1. Order Items")
                        print("2. Logout")
                        user_choice = input("Enter your choice: ")
                        if user_choice == '1':
                            order_items()
                        elif user_choice == '2':
                            logout_user()
                            break
                        else:
                            print("Invalid choice. Please try again.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
