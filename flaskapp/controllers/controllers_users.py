from flaskapp import app
from flask import render_template, redirect, session, request, flash
from flaskapp.models.models_user import User
from flask_bcrypt import Bcrypt
from flaskapp.config.mysqlconnection import connectToMySQL
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/user_register', methods=['POST'])
def register_user():
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : request.form['password'],
        'confirm_password' : request.form['confirm_password'],
    }
    valid = User.user_validator(data)
    if valid :
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data['pw_hash'] = pw_hash
        user = User.create_user(data)
        session['user_id'] = user
        print('You got it, You are a new user')
        return redirect('/select')
    return redirect('/register')

@app.route('/user_login', methods=['POST'])
def login_user():
    user = User.get_by_email(request.form)
    if not user:
        flash('Invalid email or password', 'login')
        return redirect('/login')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid email or password', 'login')
        return redirect('/login')
    session['user_id'] = user.id
    print('Success')
    return redirect('/select')

# Customers List -----
@app.route('/customers')
def customers():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id': session['user_id']
    }
    user = User.get_one(user_data)
    users = User.get_all()
    return render_template('customers.html', user = user, users = users)

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')