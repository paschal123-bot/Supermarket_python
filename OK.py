import csv
import re
from tabulate import tabulate

class User:
    ROLES = ['CEO', 'admin', 'buyer']

    def __init__(self, firstName, lastName, email, password, role="buyer"):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
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

user_dict = {}
item_dict = {}
session = None

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

def load_users_from_file():
    try:
        with open('users.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user = User.from_dict(row)
                user_dict[user.email] = user
    except FileNotFoundError:
        pass

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

def save_items_to_file():
    with open('items.csv', mode='w', newline='') as file:
        fieldnames = ['Name', 'Category', 'Price', 'Quantity']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for item in item_dict.values():
            writer.writerow(item.to_dict())

def logout_user():
    global session
    session = None  # Clear the session
    print("Logout successful.")
    main_menu()  # Redirect back to the main menu

class CEO:
    def add_admin(self):
        first_name, last_name, email = self.get_user_input()
        password = input("Enter password for admin: ")
        admin = User(first_name, last_name, email, password, "admin")
        user_dict[email] = admin
        save_user_to_file_as_dict(admin)
        print(f"Admin {first_name} {last_name} added successfully.")

    def remove_admin(self):
        email = input("Enter admin email to remove: ")
        if email in user_dict and user_dict[email].role == "admin":
            del user_dict[email]
            self.save_all_users()
            print(f"Admin {email} removed successfully.")
        else:
            print("Admin not found.")

    def monitor_admins(self):
        table = [[user.firstName, user.lastName, user.email] for user in user_dict.values() if user.role == "admin"]
        headers = ["First Name", "Last Name", "Email"]
        print(tabulate(table, headers, tablefmt="grid"))

    def get_user_input(self):
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        while True:
            email = input("Enter Email: ")
            if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return first_name, last_name, email
            else:
                print("Invalid email format. Please try again.")

    def save_all_users(self):
        with open('users.csv', mode='w', newline='') as file:
            fieldnames = ['First Name', 'Last Name', 'Email', 'Password', 'Role']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for user in user_dict.values():
                writer.writerow(user.to_dict())

    def ceo_menu(self):
        while True:
            print("\n--- CEO Menu ---")
            print("1. Add Admin")
            print("2. Remove Admin")
            print("3. Monitor Admins")
            print("4. Logout")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.add_admin()
            elif choice == '2':
                self.remove_admin()
            elif choice == '3':
                self.monitor_admins()
            elif choice == '4':
                logout_user()
                break
            else:
                print("Invalid choice. Please try again.")

class Admin:
    def display_items(self):
        table = [[item.name, item.category, item.price, item.quantity] for item in item_dict.values()]
        headers = ["Name", "Category", "Price", "Quantity"]
        print(tabulate(table, headers, tablefmt="grid"))

    def add_item(self):
        name = input("Enter the name of the item: ")
        category = input("Enter the category of the item: ")
        price = int(input("Enter the price of the item: "))
        quantity = int(input("Enter the quantity of the item: "))
        new_item = Items(name, category, price, quantity)
        item_dict[name] = new_item
        save_items_to_file()
        print(f"Item {name} added successfully.")

    def record_sales(self):
        item_name = input("Enter the name of the item sold: ")
        item = item_dict.get(item_name)
        if item:
            quantity = int(input(f"Enter quantity of {item.name} sold: "))
            if quantity <= item.quantity:
                item.quantity -= quantity
                save_items_to_file()
                print(f"Recorded sale of {quantity} {item.name}.")
            else:
                print("Insufficient stock.")
        else:
            print("Item not found.")

    def admin_menu(self):
        while True:
            print("\n--- Admin Menu ---")
            print("1. Display Items")
            print("2. Add Item")
            print("3. Record Sales")
            print("4. Logout")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.display_items()
            elif choice == '2':
                self.add_item()
            elif choice == '3':
                self.record_sales()
            elif choice == '4':
                logout_user()
                break
            else:
                print("Invalid choice. Please try again.")

class Buyer:
    def order_items(self):
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
                    save_items_to_file()
                else:
                    print("Insufficient stock.")
            else:
                print("Item not found.")
            more = input("Do you want to order another item? (yes/no): ").lower()
            if more == 'no':
                break
        print(f"Total Cost: {total_cost}")
        print("Thanks for visiting Paschal's Supermarket")

    def buyer_menu(self):
        while True:
            print("\n--- Buyer Menu ---")
            print("1. Order Items")
            print("2. Logout")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.order_items()
            elif choice == '2':
                logout_user()
                break
            else:
                print("Invalid choice. Please try again.")

def login():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    user = user_dict.get(email)
    if user and user.password == password:
        print(f"Welcome {user.firstName} {user.lastName}!")
        return user
    else:
        print("Invalid email or password.")
        return None

def main_menu():
    while True:
        print("\n--- Main Menu ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            register_user()
        elif choice == '2':
            user = login()
            if user:
                global session
                session = user
                if user.role == 'CEO':
                    ceo = CEO()
                    ceo.ceo_menu()
                elif user.role == 'admin':
                    admin = Admin()
                    admin.admin_menu()
                elif user.role == 'buyer':
                    buyer = Buyer()
                    buyer.buyer_menu()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    load_users_from_file()
    initialize_supermarket()
    main_menu()

if __name__ == "__main__":
    main()
