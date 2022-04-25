from flask import Blueprint, flash, redirect, render_template, request
from quiz_application.auth import is_admin

from quiz_application.models import User
from . import db


admin = Blueprint('admin', __name__)

@admin.route('/delete_user/<int:id>')
@is_admin
def delete(id):
    user_to_delete = User.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("Successfully deleted!", category="success")
        return redirect('/admin')
    except:
        flash("Something went wrong!", category="error")
        return redirect("/admin")

@admin.route('/update_user/<int:id>', methods=['GET', 'POST']) 
@is_admin
def update_user_view(id):
    user_to_update = User.query.get_or_404(id) 
    if request.method == "POST":
        user_to_update.name = request.form['name']
        user_to_update.email = request.form['email']
        if not request.form['role']:
            user_to_update.role = "pending"    
        user_to_update.role = request.form['role'] 
        try:
            db.session.commit()
            flash("User updated successfully!", category='success')
            return redirect('/admin')
        except:
            flash("Couldn't update user", category="error")
    return render_template("/pages/admin/update_user.html", user = user_to_update)