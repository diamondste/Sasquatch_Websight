from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.sight import Sight

@app.route('/new/sight')
def new_sight():
    if 'user_id' not in session: 
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template('new_sight.html', user = User.get_one(data))

@app.route('/create/sight', methods=['POST'])
def create_sight():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Sight.validate_sight(request.form):
        return redirect('/new/sight')
    
    data = { 
        "location": request.form['location'],
        "date_seen": request.form['date_seen'],
        "happened": request.form['happened'],
        "num_sasq": int(request.form['num_sasq']),
        "user_id": session['user_id']
    }

    Sight.save(data)
    return redirect('/dashboard')

@app.route('/edit/sight/<int:id>')
def edit(id):
    if 'user_id' not in session: 
        return redirect('/logout')
    data = { 
        "id" : id
    }
    user_data = { 
        "id" : session['user_id']
    }
    return render_template("edit_sight.html", edit = Sight.get_by_id(data), user = User.get_one(user_data))

@app.route('/sight/<int:id>')
def show_sight(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = { 
        "id" : id
    }
    user_data = { 
        "id" : session['user_id']
    }
    return render_template("show_sight.html", sight = Sight.get_by_id(data), user = User.get_one(user_data), sights = Sight.get_user_report())

@app.route('/update/sight', methods=['POST'])
def update(): 
    if 'user_id' not in session: 
        return redirect('/logout')
    if not Sight.validate_sight(request.form):
        return redirect('/edit/sight/')
    
    data = { 
        "location": request.form['location'],
        "date_seen": request.form['date_seen'],
        "happened": request.form['happened'],
        "num_sasq": int(request.form['num_sasq']),
        "id": request.form['id']
    }

    Sight.update(data)
    return redirect('/dashboard')

@app.route('/destroy/sight/<int:id>')
def destroy(id): 
    if 'user_id' not in session:
        return redirect('/logout')
    data = { 
        'id' : id
    }

    Sight.destroy(data)
    return redirect('/dashboard')