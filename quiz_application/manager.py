from flask import Blueprint, flash, redirect, render_template, request
from flask_login import current_user, login_required
from quiz_application.auth import is_manager

from quiz_application.models import Question, Subject, User 
from . import db


manager = Blueprint('manager', __name__)

@manager.route("manage-subjects")
@login_required
@is_manager
def manage_subjects():
    subjects = Subject.query.all()
    return render_template("manager/manager.html", user=current_user, subjects=subjects)

@manager.route('create-subject', methods=['GET', 'POST'])
@login_required
@is_manager
def create_subject(): 
    if request.method == 'POST':
        subject_name = request.form.get('name')
        about = request.form.get('about')
        new_subject = Subject (name=subject_name, about=about, manager_id=current_user.id)
        db.session.add(new_subject)
        db.session.commit()
        flash("Success!", category='success') 
        return redirect('/manager/manage-subjects')
    return render_template('/manager/create-subject.html', user=current_user)

@manager.route('update-subject/<int:id>', methods=['GET', 'POST'])
@login_required
@is_manager
def update_subject(id): 
    subject_to_update = Subject.query.get_or_404(id)
    if subject_to_update.manager_id == current_user.id:
        if request.method == 'POST':
            subject_to_update.name = request.form.get('name')
            subject_to_update.about = request.form.get('about')
            try:
                db.session.commit()
                flash("Subject updated successfully!", category='success')
                return redirect('/manager/manage-subjects')
            except:
                flash("Couldn't update subject", category="error")  
    else:
        flash("You can only update your subject", category="error")
        return redirect("/manager/") 
    return render_template('/manager/update-subject.html', user=current_user, subject=subject_to_update)
     
@manager.route('delete-subject/<int:id>')
@login_required
@is_manager
def delete_subject(id):
    subject_to_delete = Subject.query.get_or_404(id)
    if subject_to_delete.manager_id == current_user.id:
        try:
            db.session.delete(subject_to_delete)
            db.session.commit()
            flash("Successfully deleted!", category="success")
            return redirect("/manager/manage-subjects")
        except:
            flash("Something went wrong!", category="error")
            return redirect("manager/manage-subjects")
    else:
        flash("You can only delete your subjects", category="error")
        return redirect("/manager/manage-subjects")

@manager.route('/manage-questions')
@login_required
@is_manager
def manage_questions():
    questions = Question.query.all()
    return render_template("/manager/manage-questions.html", questions=questions,user=current_user)

@manager.route("create-question", methods=['GET', 'POST'])
@login_required
@is_manager
def create_question():
    subjects = Subject.query.all()
    if request.method == "POST":
        question = request.form['question']
        subject_id = request.form['subject_id']
        choice_one = request.form['choice_one']
        choice_two = request.form['choice_two']
        choice_three = request.form['choice_three']
        answer = request.form['correct_answer']
        new_question = Question(question=question, subject_id=subject_id, choice_one=choice_one, choice_two=choice_two, choice_three=choice_three, answer=answer, manager_id=current_user.id)
        db.session.add(new_question)
        db.session.commit()
        flash("Successfuly created the question!", category='success') 
        return redirect('/manager/manage-questions')
    return render_template("manager/create-question.html", subjects=subjects, user=current_user)

@manager.route("update-question/<int:id>", methods=['GET', 'POST'])
@login_required
@is_manager
def update_question(id):
    subjects = Subject.query.all()
    question_to_update = Question.query.get_or_404(id)
    if question_to_update.manager_id == current_user.id:
        if request.method == "POST":
            question_to_update.question = request.form['question']
            question_to_update.subject_id = request.form['subject_id']
            question_to_update.choice_one = request.form['choice_one']
            question_to_update.choice_two = request.form['choice_two']
            question_to_update.choice_three = request.form['choice_three']
            question_to_update.answer = request.form['correct_answer']
            try: 
                db.session.commit()
                flash("Successfully updated question!", category='success') 
                return redirect('/manager/manage-questions')
            except:
                flash("something went wrong!", category="error")
    else:
        flash("You can only update your question!", category="error")
        return redirect("/manager/manage-questions")
    return render_template("manager/update-question.html", question=question_to_update , subjects=subjects, user=current_user)

@manager.route("delete-question/<int:id>")
@login_required
@is_manager
def delete_question(id):
    question_to_delete = Question.query.get_or_404(id)
    if question_to_delete.manager_id == current_user.id: 
        try:
            db.session.delete(question_to_delete)
            db.session.commit()
            flash("Successfully deleted!", category="success")
            return redirect('/manager/manage-questions')
        except:
            flash("Something went wrong!", category="error")
    else:
        flash("You can only delete your questions", category="error")
        return redirect("/manager/manage-questions")

@manager.route("/students-list")
@login_required
@is_manager
def see_students():
    students = User.query.filter_by(role="Student").all()
    return render_template("manager/students-list.html", user=current_user, students=students)

@manager.route("/students-list/results/<int:id>")
@login_required
@is_manager
def see_students_marks(id):
    student = User.query.get_or_404(id)
    marks = student.marks
    return render_template("manager/students-results.html", user=current_user, student=student, marks=marks)
    