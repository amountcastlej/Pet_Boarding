from flaskapp import app
from flask import render_template, redirect, session, request
from flaskapp.models.models_user import User
from flaskapp.models.models_pet import Pet
from flaskapp.config.mysqlconnection import connectToMySQL
from datetime import datetime
from pprint import pprint

now = datetime.now() # current date and time
time = now.strftime("%H")
date = now.strftime("%m.%d.%Y")

# Dashboard
@app.route('/select')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id': session['user_id']
    }
    user = User.get_one(user_data)
    return render_template('select.html', user= user, time = time, date = date)

@app.route('/cats')
def cats():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id': session['user_id']
    }
    user = User.get_one(user_data)
    all_likes = Pet.get_all_who_liked()
    return render_template('cats.html', user= user, all_likes = all_likes)

@app.route('/dogs')
def dogs():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id': session['user_id']
    }
    user = User.get_one(user_data)
    all_likes = Pet.get_all_who_liked()
    return render_template('dogs.html', user= user, all_likes = all_likes)

# Create Animal Page -----
@app.route('/add_pet')
def add_pet():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('new_pet.html')

# Create Animal Add To Database -----
@app.route('/create_pet', methods=['POST'])
def create_pet():
    data = {
        'type' : request.form['type'],
        'name' : request.form['name'],
        'breed' : request.form['breed'],
        'dob' : request.form['dob'],
        'gender' : request.form['gender'],
        'hair_color' : request.form['hair_color'],
        'information' : request.form['information'],
        'user_id' : session['user_id']
    }
    Pet.create_pet(data)
    return redirect('/select')

# Display One Aminal -----
@app.route('/show_pet/<int:pet_id>')
def show_pet(pet_id):
    data = {
        'id' : pet_id
    }
    pet = Pet.get_one(data)
    all = Pet.all_pets()
    return render_template('one_pet.html', pet = pet, all = all)

# Edit One Animal -----
@app.route('/edit_pet/<int:pet_id>')
def edit_pet(pet_id):
    data = {
        'id' : pet_id
    }
    pet = Pet.get_one(data)
    return render_template('edit_pet.html', pet = pet)

# Update One Animal -----
@app.route('/update_pet/<int:pet_id>', methods=['POST'])
def update_pet(pet_id):
    Pet.update_pet(request.form, pet_id)
    return redirect('/select')

# Moved to controllers_likes,py
# Like One Pet -----
@app.route('/like/<int:pet_id>')
def like(pet_id):
    data = {
        'pet_id' : pet_id,
        'user_id' : session['user_id']
    }
    Pet.like(data)
    return redirect('/select')

# Dislike One Pet -----
@app.route('/dislike/<int:pet_id>')
def dislike(pet_id):
    data = {
        'pet_id' : pet_id,
        'user_id' : session['user_id']
    }
    Pet.dislike(data)
    return redirect('/select')

# Delete One Animal -----
@app.route('/delete/<int:pet_id>')
def delete(pet_id):
    data = {
        'id' : pet_id
    }
    Pet.delete_pet(data)
    return redirect('/select')