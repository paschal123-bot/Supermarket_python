from flask import Flask, render_template, redirect, url_for, request, session
from models import User, Student, Teacher, Class

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize some lists to store users, students, teachers, and classes
users = []
students = []
teachers = []
classes = []

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
        users.append(user)
        return redirect(url_for('login_user'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        for user in users:
            if user.email == email and user.password == password:
                session['user'] = user.to_dict()
                return redirect(url_for('dashboard'))
        return "Invalid email or password."
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login_user'))
    return render_template('dashboard.html')

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
        
        account_number = request.form
