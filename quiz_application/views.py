from re import sub
from unicodedata import category
from flask import Blueprint, flash, redirect, render_template, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from quiz_application.auth import is_admin, is_manager, redirecting_users
from . import db
from quiz_application.models import Subject, User

views = Blueprint('views', __name__)

# homepage route for unauthenticated users
@views.route('/') 
def home():
    return render_template("pages/home.html", user=current_user)

# students will be directed to this route
@views.route('/student')
@login_required
def student():
    student_subjects = current_user.subjects
    all_subjects = Subject.query.all() 
    marks = current_user.marks 
    return render_template("pages/student/student.html", user=current_user, subjects=student_subjects, marks=marks, all_subjects=all_subjects)

# admins will be directed to this route    
@views.route('/admin')
@login_required
@is_admin
def admin():
    users = User.query.all()
    return render_template("pages/admin/admin.html", user = current_user, users = users)
    
@views.route('/pending_user')
@login_required
def pending():
    return render_template("pages/pendingUser.html", user=current_user)

@views.route('/edit_profile', methods=["GET", "POST"])
@login_required
def update_profile():
    update_self = User.query.get_or_404(current_user.id) 
    if request.method == "POST":
        update_self.name = request.form['name']
        update_self.email = request.form['email']  
        if request.form['password']: 
            if request.form['password'] != request.form['confirm_password']:
                flash("Password did not match the confirm the password!", category='error')
            elif request.form['password'] and request.form['password'] == request.form['confirm_password']:
                update_self.password = generate_password_hash(request.form['password'], method="sha256") 
                try:
                    db.session.commit()
                    flash("Profile updated successfully!", category='success')
                    return redirecting_users(update_self.role)
                except:
                    flash("Couldn't edit profile!", category="error")  
            else:
                flash("Please Fill in the required fields properly",category='error')
        else:
            try:
                db.session.commit()
                flash("Profile updated successfully!", category='success')
                return redirecting_users(update_self.role)
            except:
                flash("Couldn't edit profile!", category="error")  
    return render_template("/pages/edit_profile.html", user = current_user)

@views.route('/manager')  
@is_manager  
@login_required
def manager():
    subjects = Subject.query.all()
    return render_template("pages/manager/manager.html", user = current_user, subjects = subjects)

