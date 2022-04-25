from functools import wraps
from flask import Blueprint, flash, redirect, render_template, request
from quiz_application.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user 

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged In Successfully!", category="success")
                login_user(user, remember=True)
                return redirecting_users(user.role)
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash("Email doesn't exist!", category='error')
    return render_template('auth/login.html', user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!', category='error')
        elif not email:
            flash("Please provide a valid email", category='error')
        elif not password:
            flash("Please enter a password", category='error')
        elif password != confirm_password:
            flash("Please confirm the password!", category='error')
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Success!", category='success')
            login_user(new_user, remember=True)
            return redirect('/pending_user')
            
    return render_template('auth/sign_up.html', user = current_user)

def redirecting_users(role):
    if role == "Admin":
        return redirect('/admin')
    elif role == "Pending":
        return redirect('/pending_user')
    elif role == "Student":
        return redirect("/student")
    elif role == "Manager":
        return redirect("/manager")
    else: 
        return redirect('/')

def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.role == "Admin":
            return f(*args, **kwargs)
        else:
            flash("Unauthorized", category="error")
            return redirect("/") 
    return wrap
    
def is_manager(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.role == "Manager":
            return f(*args, **kwargs)
        else:
            flash("Unauthorized", category="error")
            return redirect("/") 
    return wrap