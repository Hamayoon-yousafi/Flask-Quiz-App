from flask import Blueprint, flash, redirect, render_template, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from quiz_application.auth import is_admin, is_manager, is_student, redirecting_users
from . import db
from quiz_application.models import Subject, User

views = Blueprint('views', __name__)

# homepage route for unauthenticated users
@views.route('/') 
def home():
    return render_template("/sharedviews/home.html", user=current_user)

# students will be directed to this route
@views.route('/student')
@is_student
@login_required
def student():
    student_subjects = current_user.subjects 
    return render_template("/student/portal.html", user=current_user, subjects=student_subjects)

# admins will be directed to this route    
@views.route('/admin')
@is_admin
@login_required
@is_admin
def admin():
    return render_template("/admin/portal.html", user = current_user)
    
@views.route('/pending_user')
@login_required
def pending():
    return render_template("sharedviews/pendingUser.html", user=current_user)

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
    return render_template("sharedviews/edit_profile.html", user = current_user)

@views.route("/delete_self")
@login_required
def delete():
    try:
        db.session.delete(current_user)
        db.session.commit()
        flash("Successfully deleted!", category="success") 
        return redirect("/")
    except:
        flash("Something went wrong!", category="error") 

@views.route('/manager')  
@is_manager  
@login_required
def manager(): 
    return render_template("/manager/portal.html", user = current_user)

