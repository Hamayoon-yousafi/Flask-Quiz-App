from flask import Blueprint, flash, render_template, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from quiz_application.auth import is_admin, is_manager, is_student
from . import db
from quiz_application.models import Subject, User

views = Blueprint('views', __name__)

# homepage route for unauthenticated users
@views.route('/') 
def home():
    return render_template("/sharedviews/home.html", user=current_user)

# students will be directed to this route
@views.route('/student')
@login_required
@is_student
def student():
    student_subjects = current_user.subjects 
    return render_template("/student/portal.html", user=current_user, subjects=student_subjects)

# admins will be directed to this route    
@views.route('/admin')
@login_required
@is_admin
@is_admin
def admin():
    return render_template("/admin/portal.html", user = current_user)
    
@views.route('/pending_user')
@login_required
def pending():
    return render_template("sharedviews/pendingUser.html", user=current_user)

@views.route('/manager')  
@login_required
@is_manager  
def manager(): 
    return render_template("/manager/portal.html", user = current_user)

