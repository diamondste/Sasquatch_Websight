from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.sight import Sight
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("register.html")

@app.route('/register', methods=['POST'])
def register():
    if not User.validate(request.form):
        return redirect('/')

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : bcrypt.generate_password_hash(request.form['password'])
    }

    id = User.save(data)

    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if (request.method == 'POST'):
        user = User.get_by_email(request.form)

        if not user:
            flash("Invalid Email/Password", "login")
            return redirect('/login')
        if not bcrypt.check_password_hash(user.password, request.form['password']):

            flash("Invalid Email/Password", "login")
            return redirect('/login')
        session['user_id'] = user.id
        return redirect('/dashboard')
    return render_template("login.html")


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }

    return render_template('dashboard.html', user = User.get_one(data), sights = Sight.get_user_report())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')