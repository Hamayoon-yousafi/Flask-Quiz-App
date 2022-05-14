from flask import Blueprint, flash, redirect, render_template, request
from flask_login import current_user, login_required
from quiz_application.auth import is_admin
from quiz_application.forms import UpdateUserForm
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
    user_to_delete = User.query.get_or_404(id)
    if user_to_delete.role != "Admin":
        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("Successfully deleted!", category="success")
            return redirect('/admin/users-list')
        except:
            flash("Something went wrong!", category="error")
            return redirect("/admin")
    else:
        flash("You cannot delete admin", category="error")
        return redirect("/admin/users-list")

@admin.route('/update_user/<int:id>', methods=['GET', 'POST']) 
@login_required
@is_admin 
def update_user(id):
    user_to_update = User.query.get_or_404(id) 
    form = UpdateUserForm(request.form)  
    roles = ["Admin", "Student", "Manager", "Pending"]
    form.role.choices.insert(0, user_to_update.role) 
    for role in roles:
        if user_to_update.role != role:
            form.role.choices.append(role)

    if request.method == "POST" and form.validate():
        user_to_update.name = form.name.data
        user_to_update.email = form.email.data    
        user_to_update.role = form.role.data 
        assignments(user_to_update, form)
        try:
            db.session.commit()
            flash("User updated successfully!", category='success')
            return redirect('/admin/users-list')
        except:
            flash("Couldn't update user", category="error")
    return render_template("/admin/update_user.html", user=user_to_update, form=form) 