from flask import Flask, request, jsonify, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        
        if password != confirm_password:
            return "Passwords do not match. Please try again."
        user = User(first_name, last_name, email, password)
        user_list.append(user)
        return redirect(url_for('login_user'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        for user in user_list:
            if user.email == email and user.password == password:
                session['user'] = user.to_dict()
                return redirect(url_for('order_items'))
        return "Invalid email or password."
    return render_template('login.html')

@app.route('/items')
def display_items():
    items = [item.to_dict() for item in item_list]
    return jsonify(items)

@app.route('/order', methods=['GET', 'POST'])
def order_items():
    if 'user' not in session:
        return redirect(url_for('login_user'))
    
    if request.method == 'POST':
        cart = []
        total_cost = 0
        for item_name, quantity in request.form.items():
            quantity = int(quantity)
            item = search_item(item_name)
            if item and quantity <= item.quantity:
                cart.append((item, quantity))
                total_cost += item.price * quantity
                item.quantity -= quantity
            else:
                return "Insufficient stock or item not found."
        
        account_number = request.form['accountNumber']
        return f"Payment of {total_cost} successful to account number {account_number}."
    
    return render_template('order.html', items=item_list)

def search_item(name):
    for item in item_list:
        if item.name.lower() == name.lower():
            return item
    return None

if __name__ == "__main__":
    initialize_supermarket()
    app.run(debug=True)
