from flask import Blueprint, flash, render_template, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from quiz_application.auth import is_admin, is_manager, is_student, redirecting_users
from quiz_application.forms import UpdatePasswordForm, UpdateProfileForm
from . import db 

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

@views.route('/edit_profile', methods=["GET", "POST"])
@login_required
def update_profile():
    form = UpdateProfileForm(request.form) 
    if request.method == "POST" and form.validate():   
        current_user.name = form.name.data
        current_user.email = form.email.data      
        try:
            db.session.commit()
            flash("Profile updated successfully!", category='success')
            return redirecting_users(current_user.role)
        except:
            flash("Couldn't edit profile!", category="error")   
    return render_template("sharedviews/edit_profile.html", user=current_user, form=form)

@views.route('/change-password', methods=["GET", "POST"])
@login_required
def update_password():
    form = UpdatePasswordForm(request.form)
    if request.method == "POST" and form.validate():
        if check_password_hash(current_user.password, form.password.data):
            current_user.password = generate_password_hash(form.create_password.data, method='sha256')
            try:
                db.session.commit()
                flash("Password changed successfully!", category='success')
                return redirecting_users(current_user.role)
            except:
                flash("Couldn't change password!", category="error")
            return redirecting_users(current_user.role)
        else:
            flash("You entered wrong password", category="error")
    return render_template("sharedviews/update-password.html", user=current_user, form=form)


