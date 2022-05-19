from functools import wraps 
from flask import Blueprint, flash, redirect, render_template, request
from quiz_application.forms import Login, SignupForm
from quiz_application.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user 

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login(): 
    form = Login(request.form)
    if request.method == 'POST' and form.validate(): 
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data): 
            flash("Logged In Successfully!", category="success")
            login_user(user)
            return redirecting_users(user.role)
        else:
            flash('Wrong password or email!', category='error') 
    return render_template('auth/login.html', user = current_user, form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():  
            if User.query.filter_by(email=form.email.data).first():
                flash('Email already exists!', category='error') 
                return redirect("/sign-up")
            else:
                new_user = User(email=form.email.data, name=form.name.data, password=generate_password_hash(form.create_password.data, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                flash("Success!", category='success')
                login_user(new_user, remember=True)
                return redirect('/pending_user') 
    return render_template('auth/sign_up.html', user = current_user, form=form)

# redirecting users to particular routes.
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
        if current_user.role == "Manager" or current_user.role == "Admin":
            return f(*args, **kwargs)
        else:
            flash("Unauthorized", category="error")
            return redirect("/") 
    return wrap

def is_student(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.role == "Student":
            return f(*args, **kwargs)
        else:
            flash("Unauthorized", category="error")
            return redirect("/") 
    return wrap


#, remember=True