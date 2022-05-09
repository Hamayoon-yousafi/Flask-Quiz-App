from flask import Blueprint, flash, redirect, render_template, request
from flask_login import current_user, login_required
from quiz_application.auth import is_admin
from quiz_application.models import User
from . import db

admin = Blueprint('admin', __name__)

@admin.route('/users-list') 
@login_required 
@is_admin
def users_list():
    users = User.query.all() 
    pending_users = [user for user in users if user.role == "Pending"]  
    
    return render_template("admin/admin.html", user=current_user ,users = users, pending_users = pending_users)

@admin.route('/delete_user/<int:id>')
@login_required
@is_admin
def delete(id):
    try:
        db.session.delete(User.query.get_or_404(id))
        db.session.commit()
        flash("Successfully deleted!", category="success")
        return redirect('/admin/users-list')
    except:
        flash("Something went wrong!", category="error")
        return redirect("/admin")

@admin.route('/update_user/<int:id>', methods=['GET', 'POST']) 
@login_required
@is_admin
def update_user(id):
    user_to_update = User.query.get_or_404(id) 
    if request.method == "POST":
        user_to_update.name = request.form['name']
        user_to_update.email = request.form['email']
        if not request.form['role']:
            user_to_update.role = "Pending"    
        user_to_update.role = request.form['role'] 
        try:
            db.session.commit()
            flash("User updated successfully!", category='success')
            return redirect('/admin/users-list')
        except:
            flash("Couldn't update user", category="error")
    return render_template("/admin/update_user.html", user=user_to_update)